import os
from PIL import Image
import torch
import numpy as np

class FolderLoader:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "folder_path": ("STRING", {"default": ""}),
            },
            "optional": {
                "image_load_cap": ("INT", {"default": 0, "min": 0, "step": 1}),
                "start_index": ("INT", {"default": 0, "min": 0, "step": 1}),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "load_images"
    CATEGORY = "klinter"
    NODE_COLOR = "#4169E1"  # Royal Blue
    def load_images(self, folder_path: str, image_load_cap: int = 0, start_index: int = 0) -> tuple[torch.Tensor, ...]:
        if not os.path.isdir(folder_path):
            raise FileNotFoundError(f"Folder '{folder_path}' cannot be found.")
        
        valid_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
        image_files = sorted([
            f for f in os.listdir(folder_path)
            if os.path.splitext(f.lower())[1] in valid_extensions
        ])

        image_files = image_files[start_index:]
        if image_load_cap > 0:
            image_files = image_files[:image_load_cap]

        if not image_files:
            raise ValueError("No valid images found in folder")

        images = []
        for image_path in image_files:
            full_path = os.path.join(folder_path, image_path)
            img = Image.open(full_path)
            
            if img.mode != 'RGB':
                img = img.convert('RGB')
                
            img_tensor = torch.from_numpy(np.array(img).astype(np.float32) / 255.0)
            images.append(img_tensor)

        return (torch.stack(images),)

# Register the node
NODE_CLASS_MAPPINGS = {
    "FolderLoader": FolderLoader
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FolderLoader": "Folder Loader - klinter"
}

# Export the class
__all__ = ['FolderLoader']