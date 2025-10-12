"""Node for loading images with filename output in ComfyUI."""

import os
import torch
import numpy as np
from PIL import Image, ImageOps
import folder_paths
from comfy_api.latest import io, ui

class LoadImagePlusKlinter(io.ComfyNode):
    """Node that loads an image and returns the image, mask, and filename."""
    
    @classmethod
    def define_schema(cls) -> io.Schema:
        """Define the schema for the image loading node.
        
        Returns:
            io.Schema: Node schema with inputs and outputs
        """
        input_dir = folder_paths.get_input_directory()
        files = [f for f in os.listdir(input_dir) if os.path.isfile(os.path.join(input_dir, f))]
        
        return io.Schema(
            node_id="LoadImagePlus",
            display_name="Load Image Plus - klinter",
            category="klinter",
            description="Load an image and return it along with its mask and filename",
            inputs=[
                io.Combo.Input("image", options=sorted(files)),
            ],
            outputs=[
                io.Image.Output(display_name="image"),
                io.Mask.Output(display_name="mask"),
                io.String.Output(display_name="filename")
            ]
        )

    @classmethod
    def execute(cls, image: str) -> io.NodeOutput:
        """Load an image and return it along with its mask and filename.
        
        Args:
            image: Name of the image file to load
            
        Returns:
            io.NodeOutput: Image tensor, mask, and filename without extension
        """
        image_path = folder_paths.get_annotated_filepath(image)
        i = Image.open(image_path)
        i = ImageOps.exif_transpose(i)
        img = i.convert("RGB")
        img_array = np.array(img).astype(np.float32) / 255.0
        img_tensor = torch.from_numpy(img_array)[None,]
        
        # Get filename without extension
        filename = os.path.splitext(os.path.basename(image_path))[0]
        
        # Extract alpha channel if present, otherwise create zero mask
        if i.mode == "RGBA":
            mask = torch.from_numpy(np.array(i.split()[-1]).astype(np.float32))[None,] / 255.0
        else:
            mask = torch.zeros((1, img_tensor.shape[1], img_tensor.shape[2]), dtype=torch.float32)
        
        return io.NodeOutput(img_tensor, mask, filename, ui=ui.PreviewImage(img_tensor, cls=cls))
    
    @classmethod
    def fingerprint_inputs(cls, image: str) -> str:
        """Return hash of file content for cache control.
        
        Args:
            image: Name of the image file
            
        Returns:
            str: Hash of the file for cache invalidation
        """
        image_path = folder_paths.get_annotated_filepath(image)
        return str(os.path.getmtime(image_path))

# Register the node
NODE_CLASS_MAPPINGS = {
    "LoadImagePlus": LoadImagePlusKlinter
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadImagePlus": "Load Image Plus - klinter"
}

# Export the class
__all__ = ['LoadImagePlusKlinter']
