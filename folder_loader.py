import os
from PIL import Image
import torch
import numpy as np
from comfy_api.latest import io

class FolderLoader(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        """Define the schema for the folder loader node.
        
        Returns:
            io.Schema: Node schema with inputs and outputs
        """
        return io.Schema(
            node_id="FolderLoader",
            display_name="Folder Loader - klinter",
            category="klinter",
            description="Load images from a folder",
            inputs=[
                io.String.Input("folder_path", default=""),
                io.Int.Input("image_load_cap", default=0, min=0, step=1, optional=True),
                io.Int.Input("start_index", default=0, min=0, step=1, optional=True),
            ],
            outputs=[
                io.Image.Output(display_name="images")
            ]
        )
    
    @classmethod
    def execute(cls, folder_path: str, image_load_cap: int = 0, start_index: int = 0) -> io.NodeOutput:
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

        return io.NodeOutput(torch.stack(images))

# Register the node
NODE_CLASS_MAPPINGS = {
    "FolderLoader": FolderLoader
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FolderLoader": "Folder Loader - klinter"
}

# Export the class
__all__ = ['FolderLoader']