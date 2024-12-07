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
            }
        }

    RETURN_TYPES = ("IMAGE", "MASK")
    RETURN_NAMES = ("padded_image", "mask")
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

        padded_image = torch.ones((B, new_height, new_width, C), dtype=torch.float32) * 0.5
        padded_image[:, pad_y:pad_y+H, pad_x:pad_x+W, :] = image

        if mask_feather > 0 and mask_feather * 2 < H and mask_feather * 2 < W:
            mask = torch.zeros((B, new_height, new_width), dtype=torch.float32)  # Initialize mask to zeros
            t = torch.ones_like(mask)  # Initialize t to ones
            t[:, pad_y:pad_y+H, pad_x:pad_x+W] = 0.0  # Set the area of the original image to 0.0
            
            if mask_feather > 0:
                # Create 1D Gaussian kernel
                kernel_size = mask_feather * 2 + 1
                sigma = mask_feather / 2
                kernel_1d = torch.exp(-torch.arange(-(kernel_size // 2), kernel_size // 2 + 1).float().pow(2) / (2 * sigma ** 2))
                kernel_1d = kernel_1d / kernel_1d.sum()
                
                # Create 2D kernel by outer product
                kernel_2d = torch.outer(kernel_1d, kernel_1d)
                kernel_2d = kernel_2d.view(1, 1, kernel_size, kernel_size).to(image.device)
                
                # Apply padding
                pad_size = mask_feather
                t = F.pad(t, (pad_size, pad_size, pad_size, pad_size), mode='reflect')
                
                # Apply convolution for blurring
                t = F.conv2d(t.unsqueeze(1), kernel_2d, padding=0)
                t = t.squeeze(1)
                
            mask = t  # Use the inverted mask
        else:
            mask = torch.zeros((B, new_height, new_width), dtype=torch.float32)
            mask[:, pad_y:pad_y+H, pad_x:pad_x+W] = 1.0
        
        return (padded_image, mask)

# Register the node
NODE_CLASS_MAPPINGS = {
    "OutpaintPadding": OutpaintPadding
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OutpaintPadding": "Outpaint Padding - Klinter"
}

# Export the class
__all__ = ['OutpaintPadding']
