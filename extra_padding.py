"""Extra Padding for Zoom Out node - adds padding to images for zoom out effects."""

import torch
import torch.nn.functional as F
from comfy.utils import common_upscale

class ExtraPadding:
    """
    This node is based on/inspired by the ImagePadForOutpaintMasked node by Kijai
    Modified to include zoom factor presets for easier outpainting size control
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
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("padded_image", "mask")
    FUNCTION = "expand_image"
    CATEGORY = ["image", "klinter"]
    NODE_COLOR = "#32CD32"  # Lime Green

    def expand_image(self, image, zoom_factor, mask_feather, upscale_method):
        zoom = float(zoom_factor.replace('x', ''))
        B, H, W, C = image.shape
        new_width = int(W * zoom)
        new_height = int(H * zoom)
        
        pad_x = (new_width - W) // 2
        pad_y = (new_height - H) // 2

        padded_image = torch.ones((B, new_height, new_width, C), dtype=torch.float32) * 0.5
        padded_image[:, pad_y:pad_y+H, pad_x:pad_x+W, :] = image

        if mask_feather > 0 and mask_feather * 2 < H and mask_feather * 2 < W:
            mask = torch.ones((B, new_height, new_width), dtype=torch.float32)
            t = torch.zeros_like(mask)
            t[:, pad_y:pad_y+H, pad_x:pad_x+W] = 1.0
            
            if mask_feather > 0:
                # Blur the mask
                t = t.unsqueeze(1)
                t = F.pad(t, (mask_feather, mask_feather, mask_feather, mask_feather), mode='reflect')
                t = F.gaussian_blur(t, kernel_size=mask_feather*2+1, sigma=mask_feather/2)
                t = t.squeeze(1)
                
            mask = t
        else:
            mask = torch.ones((B, new_height, new_width), dtype=torch.float32)
            mask[:, pad_y:pad_y+H, pad_x:pad_x+W] = 1.0
        
        return (padded_image, mask)

# Register the node
NODE_CLASS_MAPPINGS = {
    "ExtraPadding": ExtraPadding
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ExtraPadding": "Extra Padding - klinter"
}

# Export the class
__all__ = ['ExtraPadding']