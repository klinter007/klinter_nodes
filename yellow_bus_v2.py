import re

class YellowBusV2:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "input_1": ("*",),
                "input_2": ("*",),
                "input_3": ("*",),
                "input_4": ("*",),
                "input_5": ("*",),
                # Add more as needed
            }
        }

    RETURN_TYPES = ("*",) * 5  # Adjust this number to match the number of optional inputs
    RETURN_NAMES = tuple(f"output_{i+1}" for i in range(5))  # Adjust this number as well
    FUNCTION = "reroute"
    CATEGORY = "routing"
    NODE_COLOR = "#FFFF00"  # Yellow color

    def reroute(self, **kwargs):
        def sort_key(item):
            match = re.search(r'input_(\d+)', item[0])
            return int(match.group(1)) if match else float('inf')

        sorted_inputs = sorted(kwargs.items(), key=sort_key)
        outputs = [value for _, value in sorted_inputs if value is not None]
        
        # Pad the outputs with None to match RETURN_TYPES length
        outputs += [None] * (len(self.RETURN_TYPES) - len(outputs))
        
        return tuple(outputs)

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

NODE_CLASS_MAPPINGS = {
    "YellowBusV2": YellowBusV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "YellowBusV2": "Yellow Bus v2 🚌"
}