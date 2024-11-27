import random

class AspectSelector:
    def __init__(self):
        pass
    
    SIZES = {
        "1:1": {"width": 1536, "height": 1536},
        "3:4": {"width": 1344, "height": 1728},
        "5:8": {"width": 1248, "height": 1824},
        "9:16": {"width": 1152, "height": 2016},
        "9:21": {"width": 960, "height": 2304},
        "4:3": {"width": 1728, "height": 1344},
        "3:2": {"width": 1824, "height": 1248},
        "16:9": {"width": 2016, "height": 1152},
        "21:9": {"width": 2304, "height": 960}
    }
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "aspect_ratio": (list(cls.SIZES.keys()),),
                "control_before_generate": (["enable", "disable"], {"default": "enable"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff})
            }
        }

    RETURN_TYPES = ("INT", "INT", "STRING")
    RETURN_NAMES = ("width", "height", "name")
    FUNCTION = "return_res"
    CATEGORY = "klinter"
    OUTPUT_NODE = True

    def return_res(self, aspect_ratio, control_before_generate, seed):
        if control_before_generate == "enable":
            random.seed(seed)
            aspect_ratio = random.choice(list(self.SIZES.keys()))
        
        selected_info = self.SIZES[aspect_ratio]
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
