import random

class AspectSelector:
    def __init__(self):
        pass
    
    # Base ratios and their relative proportions (using 1536 as reference)
    BASE_RATIOS = {
        "1:1": (1.0, 1.0),
        "---": "---",
        "3:2": (1.5, 0.6667),
        "5:4": (1.25, 0.8),
        "8:5": (1.1875, 0.8125),
        "16:9": (1.3125, 0.75),
        "21:9": (1.5, 0.625),
        "---": "---",
        "2:3": (0.6667, 1.5),
        "4:5": (0.8, 1.25),
        "5:8": (0.8125, 1.1875),
        "9:16": (0.75, 1.3125),
        "9:21": (0.625, 1.5),
    }

    BASE_SIZES = {
        "512": 512,
        "768": 768,
        "1024": 1024,
        "1152": 1152,
        "1280": 1280,
        "1408": 1408,
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

    HELP = "Select base resolution (512/768/1024/1152/1280/1408/1536) and aspect ratio.\nUse seed control for random aspect ratio selection.\nOutputs optimal dimensions while maintaining selected base resolution."

    def return_res(self, base_resolution, aspect_ratio, seed):
        # If seed is not 0, use it to randomly select an aspect ratio only
        if seed != 0:
            random.seed(seed)
            aspect_ratio = random.choice([ratio for ratio in self.BASE_RATIOS.keys() if ratio != "---"])
        
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
