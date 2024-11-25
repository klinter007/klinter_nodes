# Inspired by https://github.com/mwydmuch/ZoomVideoComposer
# A node that creates a zoom-out effect transitioning between multiple images

import torch
import torch.nn.functional as F
from typing import Tuple
from math import cos, pi
from tqdm import tqdm

class ZoomOutComposer:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "images": ("IMAGE",),
                "zoom": ("FLOAT", {"default": 1.5, "min": 1.1, "max": 3.0, "step": 0.05}),
                "frames_per_transition": ("INT", {"default": 24, "min": 1, "max": 120, "step": 1}),
                "mode": (["zoom-out", "zoom-in", "zoom-out-in", "zoom-in-out"], {"default": "zoom-out"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("zoomed_frames",)
    FUNCTION = "apply_zoom"
    CATEGORY = ["image", "animation", "klinter"]
    NODE_COLOR = "#4B0082"  # Indigo color
    def easeInOutSine(self, x: float) -> float:
        return -(cos(pi * x) - 1) / 2

    def process_frame(self, i: int, images: torch.Tensor, num_frames: int, 
                     num_images: int, zoom: float) -> torch.Tensor:
        # Calculate zoom for current frame
        x = i / (num_frames - 1)
        current_zoom_log = (1 - self.easeInOutSine(x)) * num_images
        
        # Get current image index and local zoom
        current_idx = min(int(current_zoom_log), num_images)
        local_zoom = zoom ** (current_zoom_log - current_idx + 1)
        
        # Get current image
        current_image = images[current_idx]
        
        # Apply zoom through resize and center crop
        if local_zoom != 1.0:
            h, w = current_image.shape[1:3]
            new_h = int(h * local_zoom)
            new_w = int(w * local_zoom)
            
            # Resize up
            zoomed = F.interpolate(
                current_image.unsqueeze(0),
                size=(new_h, new_w),
                mode='bilinear',
                align_corners=False
            )[0]
            
            # Center crop
            start_h = (new_h - h) // 2
            start_w = (new_w - w) // 2
            zoomed = zoomed[
                :,
                start_h:start_h + h,
                start_w:start_w + w
            ]
            return zoomed
        else:
            return current_image

    def apply_zoom(self, images: torch.Tensor, zoom: float = 1.5, 
                  frames_per_transition: int = 24, mode: str = "zoom-out") -> tuple[torch.Tensor]:
        """Apply zoom effect to a sequence of images."""
        num_images = images.shape[0] - 1
        num_frames = frames_per_transition * num_images

        frames = []
        for i in tqdm(range(num_frames), desc=f"Generating {mode} frames"):
            frame = self.process_frame(i, images, num_frames, num_images, zoom)
            frames.append(frame)

        frames = torch.stack(frames)
        
        if mode == "zoom-in":
            frames = torch.flip(frames, [0])
        elif mode == "zoom-out-in":
            frames = torch.cat([frames, torch.flip(frames, [0])])
        elif mode == "zoom-in-out":
            frames = torch.cat([torch.flip(frames, [0]), frames])
            
        return (frames,)

# Register the node
NODE_CLASS_MAPPINGS = {
    "ZoomOutComposer": ZoomOutComposer
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ZoomOutComposer": "Zoom Out Composer - klinter"
}

# Export the class
__all__ = ['ZoomOutComposer']