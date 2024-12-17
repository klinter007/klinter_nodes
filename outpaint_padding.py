"""Outpaint Padding Node - adds padding around images for outpainting effects."""

import torch
import torch.nn.functional as F

class OutpaintPadding:
    """
    This node adds padding around an image for outpainting purposes.
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
            "optional": {
                "mask": ("MASK",),
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("padded_image", "mask")
    FUNCTION = "expand_image"
    CATEGORY = "klinter"
    NODE_COLOR = "#32CD32"  # Lime Green

    def expand_image(self, image, zoom_factor, mask_feather, upscale_method, mask=None):
        # Handle input mask if provided
        if mask is not None:
            if torch.allclose(mask, torch.zeros_like(mask)):
                mask = None

        zoom = float(zoom_factor.replace('x', ''))
        B, H, W, C = image.shape
        new_width = int(W * zoom)
        new_height = int(H * zoom)
        
        pad_x = (new_width - W) // 2
        pad_y = (new_height - H) // 2

        # Initialize padded image with mid-gray
        padded_image = torch.ones((B, new_height, new_width, C), dtype=torch.float32) * 0.5
        padded_image[:, pad_y:pad_y+H, pad_x:pad_x+W, :] = image

        if mask is not None:
            # If mask provided, pad it to fit new size
            mask = F.pad(mask, (pad_x, pad_x, pad_y, pad_y), mode='constant', value=0)
            mask = 1 - mask  # Invert the mask
            t = torch.zeros_like(mask)
        else:
            # Create new mask
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
                    v = v * v  # Square for smoother falloff
                    
                    if mask is None:
                        t[:, i, j] = v
                    else:
                        t[:, pad_y + i, pad_x + j] = v
        
        # Finalize mask based on whether input mask was provided
        if mask is None:
            new_mask[:, pad_y:pad_y + H, pad_x:pad_x + W] = t
            return (padded_image, new_mask,)
        else:
            return (padded_image, mask,)

# Register the node
NODE_CLASS_MAPPINGS = {
    "OutpaintPadding": OutpaintPadding
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OutpaintPadding": "Outpaint Padding - Klinter"
}

# Export the class
__all__ = ['OutpaintPadding']