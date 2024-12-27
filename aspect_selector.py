import random

class AspectSelector:
    def __init__(self):
        pass
    
    # Base ratios and their relative proportions
    BASE_RATIOS = {
        "1:1": (1.0, 1.0),
        "---": "---",
        "3:2": (1.5, 1.0),
        "5:4": (1.25, 1.0),
        "8:5": (1.6, 1.0),
        "16:9": (1.7778, 1.0),
        "21:9": (2.3333, 1.0),
        "---": "---",
        "2:3": (1.0, 1.5),
        "4:5": (1.0, 1.25),
        "5:8": (1.0, 1.6),
        "9:16": (1.0, 1.7778),
        "9:21": (1.0, 2.3333),
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
        if ratio == "---":
            return None
            
        base = self.BASE_SIZES[base_size]
        width_mult, height_mult = self.BASE_RATIOS[ratio]
        
        # Calculate dimensions while maintaining the base size as the smaller dimension
        if width_mult >= height_mult:
            height = base
            width = int(base * width_mult / height_mult)
        else:
            width = base
            height = int(base * height_mult / width_mult)
            
        # Ensure dimensions are even numbers
        width = width if width % 2 == 0 else width + 1
        height = height if height % 2 == 0 else height + 1
        
        return {
            "width": width,
            "height": height
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

    def return_res(self, base_resolution, aspect_ratio, seed):
        # If seed is not 0, use it to randomly select an aspect ratio
        if seed != 0:
            random.seed(seed)
            valid_ratios = [ratio for ratio in self.BASE_RATIOS.keys() if ratio != "---"]
            aspect_ratio = random.choice(valid_ratios)
        
        # Calculate dimensions based on selected base resolution and ratio
        selected_info = self.get_dimensions(base_resolution, aspect_ratio)
        if selected_info is None:
            return (0, 0, "invalid")
            
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