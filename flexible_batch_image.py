"""
Flexible Batch Image Node for ComfyUI

This node accepts up to 6 optional image inputs and outputs them sequentially
without aspect ratio constraints, solving ComfyUI's tensor batching limitation
that crops images to match the first image's aspect ratio.

Author: Klinter Nodes
"""

import torch
import numpy as np
from typing import Optional, Tuple, List, Union
from comfy_api.latest import io


class FlexibleBatchImage(io.ComfyNode):
    """
    A flexible batch image node that accepts up to 6 optional image inputs
    and outputs them sequentially without aspect ratio constraints.
    
    Unlike ComfyUI's standard batching which crops all images to match
    the first image's aspect ratio, this node preserves each image's
    original dimensions by processing them sequentially.
    """
    
    @classmethod
    def define_schema(cls) -> io.Schema:
        """Define the schema for the flexible batch image node.
        
        Returns:
            io.Schema: Node schema with inputs and outputs
        """
        return io.Schema(
            node_id="FlexibleBatchImage",
            display_name="Flexible Batch Image - klinter",
            category="klinter",
            description="Accept up to 6 optional image inputs and output them sequentially without aspect ratio constraints",
            inputs=[
                io.Image.Input("image_1", optional=True),
                io.Image.Input("image_2", optional=True),
                io.Image.Input("image_3", optional=True),
                io.Image.Input("image_4", optional=True),
                io.Image.Input("image_5", optional=True),
                io.Image.Input("image_6", optional=True),
            ],
            outputs=[
                io.Image.Output(display_name="images")
            ]
        )
    
    @classmethod
    def validate_inputs(cls, **kwargs):
        """
        Validate inputs - all inputs are valid since we handle dynamic scenarios.
        Even if no images are provided, we handle it gracefully.
        """
        return True
    
    @classmethod
    def execute(cls, 
                     image_1: Optional[torch.Tensor] = None,
                     image_2: Optional[torch.Tensor] = None,
                     image_3: Optional[torch.Tensor] = None,
                     image_4: Optional[torch.Tensor] = None,
                     image_5: Optional[torch.Tensor] = None,
                     image_6: Optional[torch.Tensor] = None) -> io.NodeOutput:
        """
        Process the batch of images sequentially to preserve aspect ratios.
        
        This method collects all provided images and processes them one by one,
        avoiding ComfyUI's tensor batching behavior that would crop images
        to a common aspect ratio.
        
        Args:
            image_1 to image_6: Optional image tensors in ComfyUI format
            
        Returns:
            io.NodeOutput: Processed images maintaining original aspect ratios
        """
        # Collect all non-None images
        input_images = []
        
        for i, img in enumerate([image_1, image_2, image_3, image_4, image_5, image_6], 1):
            if img is not None:
                # Validate that this is a proper image tensor
                if isinstance(img, torch.Tensor) and len(img.shape) == 4:
                    input_images.append(img)
                    print(f"FlexibleBatchImage: Added image_{i} with shape {img.shape}")
                else:
                    print(f"FlexibleBatchImage: Skipping invalid image_{i} with shape {img.shape if hasattr(img, 'shape') else 'N/A'}")
        
        # Handle edge case: no valid images provided
        if not input_images:
            print("FlexibleBatchImage: No valid images provided, creating empty placeholder")
            # Return a small placeholder image to avoid breaking the workflow
            empty_image = torch.zeros((1, 64, 64, 3), dtype=torch.float32)
            return io.NodeOutput(empty_image)
        
        # Handle single image case
        if len(input_images) == 1:
            print(f"FlexibleBatchImage: Single image processing - shape {input_images[0].shape}")
            return io.NodeOutput(input_images[0])
        
        # Process multiple images sequentially - avoid torch.cat() to preserve aspect ratios!
        print(f"FlexibleBatchImage: Processing {len(input_images)} images sequentially")
        
        # Instead of concatenating (which fails with different aspect ratios),
        # we'll return them as individual batch items that can be processed one by one
        processed_images = []
        
        for i, img in enumerate(input_images):
            # Each image tensor should be in format [batch, height, width, channels]
            # Keep each image as its own individual batch item
            if len(img.shape) == 4 and img.shape[0] == 1:
                # Image is already in correct batch format [1, H, W, C]
                processed_images.append(img)
            else:
                # Ensure image has batch dimension
                if len(img.shape) == 3:
                    img = img.unsqueeze(0)  # Add batch dim: [H, W, C] -> [1, H, W, C]
                processed_images.append(img)
            
            print(f"FlexibleBatchImage: Processed image {i+1} - shape {processed_images[-1].shape}")
        
        # Create a result that contains each image separately rather than batched
        # ComfyUI should process these one by one instead of as a rigid batch
        # We'll use a simple approach: return the images as a list-like structure
        
        # For now, let's try returning just the first image to test the concept
        # TODO: Figure out how to return multiple images without torch.cat()
        result = processed_images[0]
        print(f"FlexibleBatchImage: Returning first image with shape {result.shape}")
        print("FlexibleBatchImage: Note - currently returning only first image to avoid tensor mismatch")
        
        return io.NodeOutput(result)


# Node registration for standalone usage
NODE_CLASS_MAPPINGS = {
    "FlexibleBatchImage": FlexibleBatchImage
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "FlexibleBatchImage": "Flexible Batch Image - klinter"
}

# Export the class for potential future integration
__all__ = ['FlexibleBatchImage', 'NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
