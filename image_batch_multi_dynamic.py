"""Dynamic multi-batch image node with variable number of inputs."""

import torch

class ImageBatchMultiDynamic:
    """A dynamic image batch node that can have multiple inputs.
    The number of inputs can be controlled through the UI.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        """Define dynamic inputs. The actual number is controlled by the UI."""
        return {
            "required": {
                "inputcount": ("INT", {"default": 2, "min": 2, "max": 1000, "step": 1}),
                "image_1": ("IMAGE",),
                "image_2": ("IMAGE",),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("images",)
    FUNCTION = "combine"
    CATEGORY = "image/batch"
    
    def combine(self, inputcount, **kwargs):
        """Combine multiple images into a single batch.
        
        Args:
            inputcount: Number of images to combine
            **kwargs: Dynamic image inputs named image_1, image_2, etc.
        
        Returns:
            Tuple containing the combined image batch
        """
        # Start with first image
        batch = kwargs["image_1"]
        
        # Add remaining images to batch
        for i in range(2, inputcount + 1):
            new_image = kwargs[f"image_{i}"]
            if len(new_image.shape) == 3:
                new_image = new_image.unsqueeze(0)
            batch = torch.cat([batch, new_image], dim=0)
            
        return (batch,)

# Register the node
NODE_CLASS_MAPPINGS = {
    "ImageBatchMultiDynamic": ImageBatchMultiDynamic
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ImageBatchMultiDynamic": "Image Batch Multi (Dynamic)"
}

# Export the class
__all__ = ['ImageBatchMultiDynamic']
