"""
Standalone Pixel Snapper Node for ComfyUI
Snaps pixels to perfect grid and quantizes colors for AI-generated pixel art

Based on Sprite Fusion Pixel Snapper concept
"""

import torch
import numpy as np
from PIL import Image
from comfy_api.latest import ComfyExtension, io, ui


class PixelSnapper(io.ComfyNode):
    """Snap pixels to grid and quantize colors for pixel-perfect art."""
    
    @classmethod
    def define_schema(cls) -> io.Schema:
        """Define the schema for the pixel snapper node.
        
        Returns:
            io.Schema: Node schema with inputs and outputs
        """
        return io.Schema(
            node_id="PixelSnapper",
            display_name="Pixel Snapper - klinter",
            category="klinter/image",
            description="Snap pixels to perfect grid and quantize colors for AI pixel art",
            inputs=[
                io.Image.Input("image"),
                io.Int.Input("grid_size", default=4, min=1, max=32, step=1),
                io.Int.Input("num_colors", default=16, min=2, max=256, step=1),
                io.Combo.Input("quantization_method", 
                    options=["median-cut", "octree", "max-coverage"],
                    default="median-cut"),
                io.Combo.Input("dither_method",
                    options=["none", "floyd-steinberg"],
                    default="floyd-steinberg"),
            ],
            outputs=[
                io.Image.Output(display_name="snapped_image")
            ]
        )
    
    @classmethod
    def tensor_to_pil(cls, tensor: torch.Tensor) -> Image.Image:
        """Convert ComfyUI tensor to PIL Image.
        
        Args:
            tensor: ComfyUI image tensor in format [B, H, W, C] with values 0-1
            
        Returns:
            PIL Image from first batch item
        """
        # Handle batch dimension - take first image if batched
        if tensor.ndim == 4:
            tensor = tensor[0]  # Take first image from batch
        elif tensor.ndim != 3:
            raise ValueError(f"Expected tensor with 3 or 4 dimensions, got {tensor.ndim}")
        
        # Convert to numpy array
        img_np = tensor.cpu().numpy()
        
        # Scale from 0-1 to 0-255
        img_np = (img_np * 255).astype(np.uint8)
        
        # Ensure we have 3 channels (RGB)
        if img_np.shape[2] == 1:
            # Grayscale - convert to RGB
            img_np = np.concatenate([img_np] * 3, axis=2)
        elif img_np.shape[2] == 4:
            # RGBA - for now just take RGB, could preserve alpha later
            img_np = img_np[:, :, :3]
        
        # Create PIL Image
        pil_image = Image.fromarray(img_np, 'RGB')
        return pil_image
    
    @classmethod
    def pil_to_tensor(cls, pil_image: Image.Image) -> torch.Tensor:
        """Convert PIL Image to ComfyUI tensor.
        
        Args:
            pil_image: PIL Image in RGB or RGBA mode
            
        Returns:
            torch.Tensor: Image tensor in format [1, H, W, C] with values 0-1
        """
        # Ensure RGB mode
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        
        # Convert to numpy array
        img_np = np.array(pil_image).astype(np.float32)
        
        # Normalize to 0-1 range
        img_np = img_np / 255.0
        
        # Convert to tensor and add batch dimension [H, W, C] -> [1, H, W, C]
        tensor = torch.from_numpy(img_np).unsqueeze(0)
        
        return tensor
    
    @classmethod
    def execute(cls, image: torch.Tensor, grid_size: int, num_colors: int,
                quantization_method: str, dither_method: str) -> io.NodeOutput:
        """Execute pixel snapping on the input image.
        
        Args:
            image: Input image tensor
            grid_size: Size of each pixel in the grid (1-32)
            num_colors: Number of colors in the palette (2-256)
            quantization_method: Color quantization algorithm
            dither_method: Dithering method to use
            
        Returns:
            io.NodeOutput: Pixel-snapped image with preview
        """
        try:
            # Step 1: Convert tensor to PIL Image
            pil_image = cls.tensor_to_pil(image)
            original_width, original_height = pil_image.size
            
            print(f"PixelSnapper: Processing {original_width}x{original_height} image")
            print(f"  Grid size: {grid_size}px, Colors: {num_colors}, Method: {quantization_method}, Dither: {dither_method}")
            
            # Step 2: Downsample to grid resolution
            grid_width = max(1, original_width // grid_size)
            grid_height = max(1, original_height // grid_size)
            
            print(f"  Downsampling to grid: {grid_width}x{grid_height}")
            downsampled = pil_image.resize((grid_width, grid_height), Image.LANCZOS)
            
            # Step 3: Apply color quantization
            # Map quantization method to PIL constant
            quant_map = {
                "median-cut": Image.MEDIANCUT,
                "octree": Image.FASTOCTREE,
                "max-coverage": Image.MAXCOVERAGE
            }
            
            # Map dither method to PIL constant
            dither_map = {
                "none": Image.NONE,
                "floyd-steinberg": Image.FLOYDSTEINBERG
            }
            
            quant_method = quant_map.get(quantization_method, Image.MEDIANCUT)
            dither_option = dither_map.get(dither_method, Image.FLOYDSTEINBERG)
            
            print(f"  Quantizing to {num_colors} colors...")
            
            # Apply quantization with selected method and dithering
            # quantize() returns a palette mode image (P mode)
            quantized = downsampled.quantize(
                colors=num_colors,
                method=quant_method,
                dither=dither_option
            )
            
            # Convert back to RGB to ensure compatibility
            quantized_rgb = quantized.convert('RGB')
            
            # Step 4: Upsample back to original size with nearest neighbor
            # This maintains the pixel grid and creates the "snapped" look
            print(f"  Upsampling back to {original_width}x{original_height} with nearest neighbor")
            snapped = quantized_rgb.resize((original_width, original_height), Image.NEAREST)
            
            # Step 5: Convert back to ComfyUI tensor
            result_tensor = cls.pil_to_tensor(snapped)
            
            print(f"  Pixel snapping complete!")
            
            # Step 6: Return with UI preview
            return io.NodeOutput(result_tensor, ui=ui.PreviewImage(result_tensor, cls=cls))
            
        except Exception as e:
            print(f"PixelSnapper Error: {str(e)}")
            # Return original image on error
            return io.NodeOutput(image, ui=ui.PreviewImage(image, cls=cls))


# V3 Registration
class PixelSnapperExtension(ComfyExtension):
    """Extension providing the PixelSnapper node."""
    
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        """Return list of nodes in this extension.
        
        Returns:
            list: PixelSnapper node class
        """
        return [PixelSnapper]


async def comfy_entrypoint() -> PixelSnapperExtension:
    """ComfyUI V3 entry point for registering the PixelSnapper node.
    
    Returns:
        PixelSnapperExtension: Extension instance
    """
    return PixelSnapperExtension()


# Legacy V1 Registration (fallback for older ComfyUI versions)
NODE_CLASS_MAPPINGS = {
    "PixelSnapper": PixelSnapper
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PixelSnapper": "Pixel Snapper - klinter"
}

# Export symbols
__all__ = ['PixelSnapper', 'PixelSnapperExtension', 'comfy_entrypoint', 'NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']




