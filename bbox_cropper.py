import torch
import numpy as np
from PIL import Image
import json

# Make sure this class name matches the one used in MAPPINGS at the bottom
class BBoxCropper:
    """
    A ComfyUI node to crop multiple regions from an input image based on bounding box data.
    Declares input as STRING to satisfy validator when upstream node declares JSON/STRING.
    Internally parses the JSON string input.
    Ensures all output crops are padded to the same size using a WHITE background.
    """
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        """
        Defines the input types for the node.
        Declaring bbox_data as STRING.
        """
        return {
            "required": {
                "image": ("IMAGE",),
                # Declaring STRING type declaration
                "bbox_data": ("STRING", {
                    "multiline": True,
                    "default": '[{"bboxes": [[10, 10, 100, 100]], "labels": ["example"]}]'
                }),
                "padding": ("INT", {
                    "default": 0,
                    "min": 0,
                    "max": 200,
                    "step": 1
                }),
            },
        }

    RETURN_TYPES = ("IMAGE", "STRING", "STRING")
    RETURN_NAMES = ("CROPPED_IMAGES", "CROPPED_LABELS", "USED_BBOXES")
    FUNCTION = "crop"
    CATEGORY = "Image/Processing" # Or your preferred category

    # --- tensor_to_pil and pil_to_tensor methods remain the same ---
    def tensor_to_pil(self, tensor):
        if tensor.ndim == 3: tensor = tensor.unsqueeze(0)
        images = []
        for i in range(tensor.shape[0]):
            img_np = tensor[i].cpu().numpy()
            img_np = (img_np * 255).astype(np.uint8)
            if img_np.ndim == 2: img_np = np.stack((img_np,)*3, axis=-1)
            elif img_np.shape[2] == 1: img_np = np.concatenate((img_np,) * 3, axis=-1)

            if img_np.shape[2] == 3: images.append(Image.fromarray(img_np, 'RGB'))
            elif img_np.shape[2] == 4: images.append(Image.fromarray(img_np, 'RGBA'))
            else: print(f"Warning: tensor_to_pil unexpected channels: {img_np.shape[2]}. Skipping.")
        return images

    def pil_to_tensor(self, pil_images):
        if not pil_images:
            print("Warning: No images provided to pil_to_tensor.")
            return torch.zeros((1, 1, 1, 3), dtype=torch.float32)

        max_width, max_height = 0, 0
        has_alpha = any(img.mode == 'RGBA' for img in pil_images)
        target_mode = 'RGBA' if has_alpha else 'RGB'
        num_channels = 4 if has_alpha else 3

        for img in pil_images:
            if img.width > max_width: max_width = img.width
            if img.height > max_height: max_height = img.height

        if max_width == 0: max_width = 1
        if max_height == 0: max_height = 1

        padding_color = (255, 255, 255, 255) if has_alpha else (255, 255, 255)
        tensors = []

        for img in pil_images:
            if img.mode != target_mode: img = img.convert(target_mode)
            padded_img = Image.new(target_mode, (max_width, max_height), padding_color)
            paste_x, paste_y = (max_width - img.width) // 2, (max_height - img.height) // 2
            if img.mode == 'RGBA': padded_img.paste(img, (paste_x, paste_y), mask=img)
            else: padded_img.paste(img, (paste_x, paste_y))
            img_np = np.array(padded_img).astype(np.float32) / 255.0
            tensors.append(torch.from_numpy(img_np).unsqueeze(0))

        if not tensors:
            print("Warning: No valid images left after processing.")
            return torch.zeros((1, max_height, max_width, num_channels), dtype=torch.float32)

        try:
            output_tensor = torch.cat(tensors, dim=0)
        except RuntimeError as e:
             print(f"------ ERROR during torch.cat ------\nShapes: {[t.shape for t in tensors]}\nMax Dims: H={max_height}, W={max_width}, C={num_channels}\nError: {e}\n------------------------------------")
             return torch.zeros((1, max_height, max_width, num_channels), dtype=torch.float32)
        return output_tensor
    # --- ---

    # Input 'bbox_data' is expected to be a string due to INPUT_TYPES declaration
    def crop(self, image: torch.Tensor, bbox_data: str, padding: int):
        """
        Crops the input image based on bounding box data provided as a JSON string.
        Pads output crops with WHITE.
        """
        data = None
        try:
            if not isinstance(bbox_data, str):
                 # Failsafe, though validation should prevent this
                 raise ValueError(f"Input bbox_data was not a string (type: {type(bbox_data).__name__})")

            # Parse the incoming JSON String
            print("Parsing bbox_data string as JSON...") # Log
            data = json.loads(bbox_data)
            print("JSON parsing successful.") # Log

            # Validate the parsed data structure
            if not isinstance(data, list) or len(data) == 0:
                raise ValueError("Parsed bbox_data must be a non-empty list.")
            if not isinstance(data[0], dict) or "bboxes" not in data[0] or "labels" not in data[0]:
                 raise ValueError("First element in parsed list must be a dict with 'bboxes' and 'labels' keys.")

            bboxes = data[0]["bboxes"]
            labels = data[0]["labels"]

            if not isinstance(bboxes, list) or not isinstance(labels, list):
                 raise ValueError("'bboxes' and 'labels' must be lists.")

            if len(bboxes) != len(labels):
                 print(f"Warning: Mismatch! BBoxes: {len(bboxes)}, Labels: {len(labels)}. Using minimum.")
                 min_len = min(len(bboxes), len(labels))
                 bboxes = bboxes[:min_len]
                 labels = labels[:min_len]

        except json.JSONDecodeError as json_e:
             print(f"!!! Error: Invalid JSON string received in bbox_data: {json_e}")
             debug_str = bbox_data[:500] + ('...' if len(bbox_data) > 500 else '')
             print(f"Received string (start): {debug_str}")
             return (torch.zeros((1, 64, 64, 3), dtype=torch.float32), "[]", "[]") # Return placeholder
        except (ValueError, TypeError, AttributeError, Exception) as e:
            print(f"!!! Error processing bbox_data input: {e}")
            return (torch.zeros((1, 64, 64, 3), dtype=torch.float32), "[]", "[]") # Return placeholder

        # --- Cropping Logic ---
        if image.shape[0] > 1: print(f"Warning: Input has {image.shape[0]} images. Processing first.")

        pil_images = self.tensor_to_pil(image[0:1])
        if not pil_images:
             print("!!! Error: Could not convert input tensor to PIL image.")
             return (torch.zeros((1, 64, 64, 3), dtype=torch.float32), "[]", "[]")

        source_pil_image = pil_images[0]
        img_width, img_height = source_pil_image.size
        cropped_pil_images, cropped_labels_list, used_bboxes_list = [], [], []
        print(f"Processing {len(bboxes)} bounding boxes...") # Log

        for i, (bbox, label) in enumerate(zip(bboxes, labels)):
            if not isinstance(bbox, list) or len(bbox) != 4:
                print(f"  Skipping invalid bbox format at index {i}: {bbox}")
                continue
            try:
                x_min, y_min, x_max, y_max = map(float, bbox)
                x_min_pad = max(0, int(x_min - padding))
                y_min_pad = max(0, int(y_min - padding))
                x_max_pad = min(img_width, int(x_max + padding))
                y_max_pad = min(img_height, int(y_max + padding))

                if x_min_pad >= x_max_pad or y_min_pad >= y_max_pad:
                    # print(f"  Skipping zero-area bbox at index {i}") # Optional log
                    continue

                cropped_img = source_pil_image.crop((x_min_pad, y_min_pad, x_max_pad, y_max_pad))

                if cropped_img.width > 0 and cropped_img.height > 0:
                    cropped_pil_images.append(cropped_img)
                    cropped_labels_list.append(label)
                    used_bboxes_list.append([x_min_pad, y_min_pad, x_max_pad, y_max_pad])
                # else: print(f"  Skipping zero-dim crop at index {i}") # Optional log

            except ValueError: print(f"!!! Warning: Non-numeric bbox skipped at index {i}: {bbox}")
            except Exception as e: print(f"!!! Error cropping bbox at index {i} ({bbox}): {e}")

        print(f"Successfully prepared {len(cropped_pil_images)} images for tensor conversion.") # Log
        output_tensor = self.pil_to_tensor(cropped_pil_images)
        labels_json = json.dumps(cropped_labels_list)
        bboxes_json = json.dumps(used_bboxes_list)

        return (output_tensor, labels_json, bboxes_json)
