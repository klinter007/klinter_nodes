import os
import json

class FluxSizeSelector:
    def __init__(self):
        self.size_options, self.size_dict = self.read_sizes()

    @classmethod
    def INPUT_TYPES(cls):
        cls.size_options, cls.size_dict = cls.read_sizes()
        return {
            'required': {
                'aspect_ratio': (list(cls.size_options.keys()),),
                'size': (["tiny", "small", "medium", "large"],),
                'orientation': (["normal", "flipped"],),
            }
        }

    RETURN_TYPES = ("INT", "INT", "STRING")
    RETURN_NAMES = ("width", "height", "description")
    FUNCTION = "select_size"
    CATEGORY = "klinter/sizing"

    @classmethod
    def read_sizes(cls):
        p = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(p, 'fluxsizes.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data['sizes'], data['sizes']

    def select_size(self, aspect_ratio, size, orientation):
        selected_size = self.size_dict[aspect_ratio][size]
        width = selected_size["width"]
        height = selected_size["height"]
        
        if orientation == "flipped":
            width, height = height, width
            flipped_ratio = ':'.join(reversed(aspect_ratio.split(':')))
            description = f"{size} {flipped_ratio} ({width}x{height})"
        else:
            description = f"{size} {aspect_ratio} ({width}x{height})"

        return (width, height, description)

# Add this to NODE_CLASS_MAPPINGS
NODE_CLASS_MAPPINGS = {
    "FluxSizeSelector": FluxSizeSelector,
}

# Add this to NODE_DISPLAY_NAME_MAPPINGS
NODE_DISPLAY_NAME_MAPPINGS = {
    "FluxSizeSelector": "Flux Size Selector (klinter)",
}