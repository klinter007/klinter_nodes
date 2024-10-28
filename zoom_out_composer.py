# Inspired by https://github.com/mwydmuch/ZoomVideoComposer
# A node that creates a zoom-out effect transitioning between multiple images

import torch
import torch.nn.functional as F
from typing import Tuple
from math import cos, pi

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
    CATEGORY = "Image Processing"

    def easeInOutSine(self, x: float) -> float:
        return -(cos(pi * x) - 1) / 2

    def process_frame(self, i: int, images: torch.Tensor, num_frames: int, 
                     num_images: int, zoom: float) -> torch.Tensor:
        print(f"\nProcessing frame {i}")
        print(f"Input images tensor shape: {images.shape}")
        
        # Calculate zoom for current frame
        x = i / (num_frames - 1)
        current_zoom_log = (1 - self.easeInOutSine(x)) * num_images
        
        # Get current image index and local zoom
        current_idx = min(int(current_zoom_log), num_images)
        local_zoom = zoom ** (current_zoom_log - current_idx + 1)
        
        # Get current image
        current_image = images[current_idx]
        print(f"Current image shape: {current_image.shape}")
        
        # Apply zoom through resize and center crop
        if local_zoom != 1.0:
            h, w = current_image.shape[1:3]
            new_h = int(h * local_zoom)
            new_w = int(w * local_zoom)
            
            # Resize up
            zoomed = F.interpolate(
                current_image.unsqueeze(0),
                size=(new_h, new_w),
                mode='bicubic',
                align_corners=False
            ).squeeze(0)
            print(f"After zoom shape: {zoomed.shape}")
            
            # Center crop back to original size
            margin_h = (new_h - h) // 2
            margin_w = (new_w - w) // 2
            zoomed = zoomed[:, margin_h:margin_h + h, margin_w:margin_w + w]
            print(f"After crop shape: {zoomed.shape}")
            
            return zoomed
        
        return current_image

    def apply_zoom(self, images: torch.Tensor, zoom: float, frames_per_transition: int, mode: str) -> Tuple[torch.Tensor]:
        print(f"\nStarting apply_zoom in {mode} mode")
        print(f"Input images shape: {images.shape}")
        
        # Move channels last to first for processing
        if len(images.shape) == 4:  # BHWC -> BCHW
            images = images.permute(0, 3, 1, 2)
            print(f"After first permute: {images.shape}")
            
        # Always reverse images for zoom out generation
        images = torch.flip(images, [0])
            
        # Calculate total frames based on transitions needed
        num_transitions = len(images) - 1
        num_frames = num_transitions * frames_per_transition
        num_images = len(images) - 1
        
        print(f"Will generate {num_frames} frames")
        
        # Generate frames (always as zoom out)
        frames = []
        for i in range(num_frames):
            frame = self.process_frame(i, images, num_frames, num_images, zoom)
            frames.append(frame)
            
        # Stack frames
        output = torch.stack(frames, dim=0)
        
        # Now handle the different modes by manipulating the complete sequence
        if mode == "zoom-in":
            output = torch.flip(output, [0])
        elif mode == "zoom-out-in":
            reverse_output = torch.flip(output, [0])
            output = torch.cat([output, reverse_output], dim=0)
        elif mode == "zoom-in-out":
            reverse_output = torch.flip(output, [0])
            output = torch.cat([reverse_output, output], dim=0)
        
        # Convert to BHWC format
        output = output.permute(0, 2, 3, 1)
        print(f"Final output shape: {output.shape}")
        
        return (output,)

# Export the class
__all__ = ['ZoomOutComposer']