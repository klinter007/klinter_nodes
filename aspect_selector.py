import random

class AspectSelector:
    def __init__(self):
        pass
    
    SIZES = {
        "1:1 square": {"width": 1536, "height": 1536, "name": "Square"},
        "3:4 portrait": {"width": 1344, "height": 1728, "name": "Portrait 3:4"},
        "5:8 portrait": {"width": 1248, "height": 1824, "name": "Portrait 5:8"},
        "9:16 portrait": {"width": 1152, "height": 2016, "name": "Portrait 9:16"},
        "9:21 portrait": {"width": 960, "height": 2304, "name": "Portrait 9:21"},
        "4:3 landscape": {"width": 1728, "height": 1344, "name": "Landscape 4:3"},
        "3:2 landscape": {"width": 1824, "height": 1248, "name": "Landscape 3:2"},
        "16:9 landscape": {"width": 2016, "height": 1152, "name": "Landscape 16:9"},
        "21:9 landscape": {"width": 2304, "height": 960, "name": "Landscape 21:9"}
    }
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "aspect_ratio": (list(cls.SIZES.keys()),),
                "random_mode": (["enable", "disable"], {"default": "disable"}),
                "seed": ("INT", {"default": 0, "min": 0, "max": 0xffffffffffffffff})
            }
        }

    RETURN_TYPES = ("INT", "INT", "STRING")
    RETURN_NAMES = ("width", "height", "name")
    FUNCTION = "return_res"
    CATEGORY = "klinter"
    OUTPUT_NODE = True

    def return_res(self, aspect_ratio, random_mode, seed):
        if random_mode == "enable":
            random.seed(seed)
            aspect_ratio = random.choice(list(self.SIZES.keys()))
        
        selected_info = self.SIZES[aspect_ratio]
        width = selected_info["width"]
        height = selected_info["height"]
        name = selected_info["name"]
        return (width, height, name)

# Register the node
NODE_CLASS_MAPPINGS = {
    "AspectSelector": AspectSelector
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AspectSelector": "Aspect Ratio Selector - klinter"
}

# Export the class
__all__ = ['AspectSelector']
