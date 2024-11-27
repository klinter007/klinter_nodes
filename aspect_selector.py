import random

class AspectSelector:
    def __init__(self):
        pass
    
    # Base ratios and their relative proportions (using 1536 as reference)
    BASE_RATIOS = {
        "1:1": (1.0, 1.0),
        "3:4": (0.875, 1.125),  # 1344/1536, 1728/1536
        "5:8": (0.8125, 1.1875),  # 1248/1536, 1824/1536
        "9:16": (0.75, 1.3125),  # 1152/1536, 2016/1536
        "9:21": (0.625, 1.5),  # 960/1536, 2304/1536
        "4:3": (1.125, 0.875),  # 1728/1536, 1344/1536
        "3:2": (1.1875, 0.8125),  # 1824/1536, 1248/1536
        "16:9": (1.3125, 0.75),  # 2016/1536, 1152/1536
        "21:9": (1.5, 0.625)  # 2304/1536, 960/1536
    }

    BASE_SIZES = {
        "512": 512,
        "768": 768,
        "1024": 1024,
        "1536": 1536
    }
    
    def get_dimensions(self, base_size, ratio):
        base = self.BASE_SIZES[base_size]
        width_mult, height_mult = self.BASE_RATIOS[ratio]
        return {
            "width": int(base * width_mult),
            "height": int(base * height_mult)
        }
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "base_resolution": (list(cls.BASE_SIZES.keys()), {"default": "1536"}),
                "aspect_ratio": (list(cls.BASE_RATIOS.keys()),),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff})
            }
        }

    RETURN_TYPES = ("INT", "INT", "STRING")
    RETURN_NAMES = ("width", "height", "name")
    FUNCTION = "return_res"
    CATEGORY = "klinter"
    OUTPUT_NODE = True

    HELP = "Select base resolution (512/768/1024/1536) and aspect ratio.\nUse seed control for random aspect ratio selection.\nOutputs optimal dimensions while maintaining selected base resolution."

    def return_res(self, base_resolution, aspect_ratio, seed):
        # If seed is not 0, use it to randomly select an aspect ratio only
        if seed != 0:
            random.seed(seed)
            aspect_ratio = random.choice(list(self.BASE_RATIOS.keys()))
        
        # Calculate dimensions based on selected base resolution and ratio
        selected_info = self.get_dimensions(base_resolution, aspect_ratio)
        width = selected_info["width"]
        height = selected_info["height"]
        return (width, height, aspect_ratio)

# Register the node
NODE_CLASS_MAPPINGS = {
    "AspectSelector": AspectSelector
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AspectSelector": "Aspect Ratio Selector - klinter"
}

# Export the class
__all__ = ['AspectSelector']
