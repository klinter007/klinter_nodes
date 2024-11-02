import torch
import torch.nn.functional as F
from comfy.utils import common_upscale

# Remove the self-import line that was here!

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
    CATEGORY = "image"

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
            
            for i in range(H):
                for j in range(W):
                    dt = i if pad_y != 0 else H
                    db = H - i if pad_y + H != new_height else H
                    dl = j if pad_x != 0 else W
                    dr = W - j if pad_x + W != new_width else W
                    d = min(dt, db, dl, dr)
                    
                    if d >= mask_feather:
                        continue
                    
                    v = (mask_feather - d) / mask_feather
                    t[:, pad_y + i, pad_x + j] = v * v
            
            mask[:, pad_y:pad_y+H, pad_x:pad_x+W] = t[:, pad_y:pad_y+H, pad_x:pad_x+W]
        else:
            mask = torch.ones((B, new_height, new_width), dtype=torch.float32)
            mask[:, pad_y:pad_y+H, pad_x:pad_x+W] = 0

        return (padded_image, mask)