"""Outpaint Padding Node - adds padding around images for outpainting effects and provides a zoomed-out option."""

import torch
import torch.nn.functional as F

class OutpaintPadding:
    """
    This node adds padding around an image for outpainting purposes.
    It returns two outputs:
      1. padded_image: The original padded image with the computed mask.
      2. zoomed_out_img: The padded image resized back to the original input dimensions.
    """
    
    upscale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "lanczos"]
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "image": ("IMAGE",),
                "zoom_factor": (["1.25x", "1.5x", "2.0x"],),
                "mask_feather": ("INT", {
                    "default": 40,
                    "min": 0,
                    "max": 100,
                    "step": 1,
                }),
                "upscale_method": (s.upscale_methods,),
            },
        }

    # Now returning three outputs: the padded image, the mask, and the zoomed out image.
    RETURN_TYPES = ("IMAGE", "IMAGE", "MASK")
    RETURN_NAMES = ("padded_image", "zoomed_out_img", "mask")
    FUNCTION = "expand_image"
    CATEGORY = "klinter"
    NODE_COLOR = "#32CD32"  # Lime Green

    def expand_image(self, image, zoom_factor, mask_feather, upscale_method):
        zoom = float(zoom_factor.replace('x', ''))
        B, H, W, C = image.shape
        new_width = int(W * zoom)
        new_height = int(H * zoom)
        
        pad_x = (new_width - W) // 2
        pad_y = (new_height - H) // 2

        # Initialize padded image with mid-gray
        padded_image = torch.ones((B, new_height, new_width, C), dtype=torch.float32) * 0.5
        padded_image[:, pad_y:pad_y+H, pad_x:pad_x+W, :] = image

        # Create new mask filled with ones and then apply feathering
        new_mask = torch.ones((B, new_height, new_width), dtype=torch.float32)
        t = torch.zeros((B, H, W), dtype=torch.float32)
            
        # Apply feathering if specified
        if mask_feather > 0 and mask_feather * 2 < H and mask_feather * 2 < W:
            for i in range(H):
                for j in range(W):
                    # Calculate distances from edges
                    dt = i if pad_y != 0 else H
                    db = H - i if pad_y != 0 else H
                    dl = j if pad_x != 0 else W
                    dr = W - j if pad_x != 0 else W
                    
                    # Find minimum distance to any edge
                    d = min(dt, db, dl, dr)
                    
                    if d >= mask_feather:
                        continue
                    
                    # Calculate and square the feather value for smooth falloff
                    v = (mask_feather - d) / mask_feather
                    t[:, i, j] = v * v
            
        new_mask[:, pad_y:pad_y + H, pad_x:pad_x + W] = t

        # Create zoomed out image: resize the padded image back to the original dimensions
        padded_tensor = padded_image.permute(0, 3, 1, 2)  # Convert to [B, C, H, W] for interpolation
        zoomed_out_tensor = F.interpolate(padded_tensor, size=(H, W), mode="bicubic", align_corners=False)
        zoomed_out_img = zoomed_out_tensor.permute(0, 2, 3, 1)  # Convert back to [B, H, W, C]

        return padded_image, new_mask, zoomed_out_img

# Register the node
NODE_CLASS_MAPPINGS = {
    "OutpaintPadding": OutpaintPadding
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OutpaintPadding": "Outpaint Padding - Klinter"
}

# Export the class
__all__ = ['OutpaintPadding']