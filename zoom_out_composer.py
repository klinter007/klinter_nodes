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
                "output_width": ("INT", {"default": 1024, "min": 16, "max": 8192, "step": 1}),
                "output_height": ("INT", {"default": 1024, "min": 16, "max": 8192, "step": 1}),
                "keep_aspect": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("zoomed_frames",)
    FUNCTION = "apply_zoom"
    CATEGORY = "klinter"
    NODE_COLOR = "#4B0082"  # Indigo color

    def easeInOutSine(self, x: float) -> float:
        return -(cos(pi * x) - 1) / 2

    def process_frame(self, i: int,
                      images: torch.Tensor,
                      num_frames: int,
                      num_images: int,
                      zoom: float) -> torch.Tensor:
        """
        Maps frame i from 0..(num_frames-1) onto an index 0..(num_images-1),
        using the easing function to distribute transitions smoothly.
        """
        # Normalized position in [0, 1].
        x = i / (num_frames - 1)
        
        # Easing value in [0, 1].
        e = self.easeInOutSine(x)

        # Map easing to 0..(num_images-1).
        current_idx_f = e * (num_images - 1)  # if we have N images, indices are 0..N-1
        current_idx = int(current_idx_f)
        current_idx = max(0, min(current_idx, num_images - 1))

        # Fraction for partial zoom between two images, if desired.
        frac = current_idx_f - current_idx

        # Compute local zoom factor (this can be adjusted if you want a different range).
        local_zoom = zoom ** (1 + frac)

        # Select the image at current_idx.
        current_image = images[current_idx].unsqueeze(0)  # [1, C, H, W]

        scale = 1 / local_zoom
        theta = torch.tensor([[scale, 0, 0],
                              [0, scale, 0]], dtype=current_image.dtype, device=current_image.device)
        theta = theta.unsqueeze(0)  # [1, 2, 3]

        grid = F.affine_grid(theta, current_image.size(), align_corners=False)
        zoomed = F.grid_sample(current_image, grid, align_corners=False)

        return zoomed.squeeze(0)

    def apply_zoom(self,
                   images: torch.Tensor,
                   zoom: float = 1.5,
                   frames_per_transition: int = 24,
                   mode: str = "zoom-out",
                   output_width: int = 1024,
                   output_height: int = 1024,
                   keep_aspect: bool = True) -> tuple[torch.Tensor]:

        # If images come in [N, H, W, C], move to [N, C, H, W].
        if images.ndim == 4:
            if images.shape[1] not in [1, 3] and images.shape[-1] in [1, 3]:
                images = images.permute(0, 3, 1, 2)
        else:
            raise ValueError("Expected images tensor of shape [N, C, H, W] or [N, H, W, C]")

        # Convert to float if needed.
        orig_dtype = images.dtype
        if not torch.is_floating_point(images):
            images = images.float() / 255.0

        # Compute desired new_width/new_height if keep_aspect is True.
        if keep_aspect:
            orig_h, orig_w = images[0].shape[1], images[0].shape[2]
            orig_ratio = orig_w / orig_h
            desired_ratio = output_width / output_height
            if desired_ratio > orig_ratio:
                new_width = int(output_height * orig_ratio)
                new_height = output_height
            else:
                new_width = output_width
                new_height = int(output_width / orig_ratio)
        else:
            new_width = output_width
            new_height = output_height

        # num_images is the total number of images you have.
        # If you have M images, indices are 0..(M-1). For transitions, you have (M-1) transitions.
        # frames_per_transition decides how long each transition is.
        # total frames = frames_per_transition * (M-1).
        num_images = images.shape[0]
        if num_images < 2:
            raise ValueError("You need at least two images for a zoom transition.")

        num_frames = frames_per_transition * (num_images - 1)

        # Generate frames using process_frame.
        frames = []
        for i in tqdm(range(num_frames), desc=f"Generating {mode} frames"):
            frame = self.process_frame(i, images, num_frames, num_images, zoom)
            frames.append(frame)

        # Stack them into [N, C, H, W].
        frames = torch.stack(frames)

        # Optionally flip or mirror frames based on the mode.
        if mode == "zoom-in":
            frames = torch.flip(frames, [0])
        elif mode == "zoom-out-in":
            frames = torch.cat([frames, torch.flip(frames, [0])])
        elif mode == "zoom-in-out":
            frames = torch.cat([torch.flip(frames, [0]), frames])

        # Resize frames.
        frames = F.interpolate(frames, size=(new_height, new_width), mode="bilinear", align_corners=False)

        # Convert back to original dtype if needed.
        if not torch.is_floating_point(torch.tensor(0, dtype=orig_dtype)):
            frames = (frames * 255).clamp(0, 255).to(orig_dtype)

        # Return in [N, H, W, C] format if ComfyUI or the subsequent node expects that.
        frames = frames.permute(0, 2, 3, 1)
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