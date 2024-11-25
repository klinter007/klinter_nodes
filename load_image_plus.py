"""Node for loading images with filename output in ComfyUI."""

import os
import torch
import numpy as np
from PIL import Image, ImageOps
import folder_paths

class LoadImagePlusKlinter:
    """Node that loads an image and returns the image, mask, and filename."""
    
    @classmethod
    def INPUT_TYPES(s):
        """Define the input types for image loading.
        
        Returns:
            dict: Input specifications including image file selection
        """
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        return {
            "required": {
                "image": (sorted(files), {"image_upload": True}),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK", "STRING")
    RETURN_NAMES = ("image", "mask", "filename")
    FUNCTION = "load_image"
    CATEGORY = "klinter"
    NODE_COLOR = "#4B0082"  # Indigo color

    def load_image(self, image: str) -> tuple[torch.Tensor, torch.Tensor, str]:
        """Load an image and return it along with its mask and filename.
        
        Args:
            image: Name of the image file to load
            
        Returns:
            tuple: (
                image tensor normalized to 0-1 range,
                alpha channel mask if present (or zero mask if not),
                filename without extension
            )
        """
        image_path = folder_paths.get_annotated_filepath(image)
        i = Image.open(image_path)
        i = ImageOps.exif_transpose(i)
        image = i.convert("RGB")
        image = np.array(image).astype(np.float32) / 255.0
        image = torch.from_numpy(image)[None,]
        
        # Get filename without extension
        filename = os.path.splitext(os.path.basename(image_path))[0]
        
        # Extract alpha channel if present, otherwise create zero mask
        if i.mode == "RGBA":
            mask = torch.from_numpy(np.array(i.split()[-1]).astype(np.float32))[None,] / 255.0
        else:
            mask = torch.zeros((1, image.shape[1], image.shape[2]), dtype=torch.float32)
        
        return (image, mask, filename)

# Register the node
NODE_CLASS_MAPPINGS = {
    "LoadImagePlus": LoadImagePlusKlinter
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadImagePlus": "Load Image Plus - klinter"
}

# Export the class
__all__ = ['LoadImagePlusKlinter']
