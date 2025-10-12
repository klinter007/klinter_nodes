"""Outpaint Padding Node - adds padding around images for outpainting effects and computes corresponding masks.

Outputs:
  1. padded_image: The original image placed onto a padded canvas.
  2. padded_mask: The mask corresponding to the padded image dimensions.
  3. zoomed out image: The padded image resized to the original image size.
  4. zoomed out mask: The padded mask resized to the original image dimensions.
"""

import torch
import torch.nn.functional as F
from comfy_api.latest import io

class OutpaintPadding(io.ComfyNode):
    """
    This node adds padding around an image for outpainting purposes.
    It returns four outputs:
      1. padded_image: The original image placed onto a padded canvas.
      2. padded_mask: The mask computed over the padded image dimensions.
      3. zoomed out image: The padded image resized to the original image size.
      4. zoomed out mask: The padded mask resized to the original image dimensions.
    """
    
    upscale_methods = ["nearest-exact", "bilinear", "area", "bicubic", "lanczos"]
    
    @classmethod
    def define_schema(cls) -> io.Schema:
        """Define the schema for the outpaint padding node.
        
        Returns:
            io.Schema: Node schema with inputs and outputs
        """
        return io.Schema(
            node_id="OutpaintPadding",
            display_name="Outpaint Padding - Klinter",
            category="klinter",
            description="Add padding around images for outpainting effects with corresponding masks",
            inputs=[
                io.Image.Input("image"),
                io.Combo.Input("zoom_factor", options=["1.25x", "1.5x", "2.0x"]),
                io.Int.Input("mask_feather", default=40, min=0, max=100, step=1),
                io.Combo.Input("upscale_method", options=cls.upscale_methods),
            ],
            outputs=[
                io.Image.Output(display_name="padded_image"),
                io.Mask.Output(display_name="padded_mask"),
                io.Image.Output(display_name="zoomed out image"),
                io.Mask.Output(display_name="zoomed out mask")
            ]
        )

    @classmethod
    def execute(cls, image, zoom_factor, mask_feather, upscale_method) -> io.NodeOutput:
        zoom = float(zoom_factor.replace('x', ''))
        B, H, W, C = image.shape
        new_width = int(W * zoom)
        new_height = int(H * zoom)
        
        pad_x = (new_width - W) // 2
        pad_y = (new_height - H) // 2

        # Initialize padded image with mid-gray
        padded_image = torch.ones((B, new_height, new_width, C), dtype=torch.float32) * 0.5
        padded_image[:, pad_y:pad_y+H, pad_x:pad_x+W, :] = image

        # Create padded_mask filled with ones and then apply feathering
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
                    t[:, i, j] = v * v
            
        new_mask[:, pad_y:pad_y + H, pad_x:pad_x + W] = t

        # Create zoomed out image: resize padded_image to original dimensions
        padded_tensor = padded_image.permute(0, 3, 1, 2)  # [B, C, new_height, new_width]
        zoomed_out_tensor = F.interpolate(padded_tensor, size=(H, W), mode="bicubic", align_corners=False)
        zoomed_out_image = zoomed_out_tensor.permute(0, 2, 3, 1)  # [B, H, W, C]

        # Create zoomed out mask: resize padded_mask to original dimensions
        mask_tensor = new_mask.unsqueeze(1)  # [B, 1, new_height, new_width]
        zoomed_mask_tensor = F.interpolate(mask_tensor, size=(H, W), mode="bicubic", align_corners=False)
        zoomed_out_mask = zoomed_mask_tensor.squeeze(1)  # [B, H, W]

        return io.NodeOutput(padded_image, new_mask, zoomed_out_image, zoomed_out_mask)

# Register the node
NODE_CLASS_MAPPINGS = {
    "OutpaintPadding": OutpaintPadding
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OutpaintPadding": "Outpaint Padding - Klinter"
}

# Export the class
__all__ = ['OutpaintPadding']