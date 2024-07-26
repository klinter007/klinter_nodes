class YellowBusV2:
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {},
            "optional": {
                "input_1": ("*",),
                "input_2": ("*",),
            }
        }

    RETURN_TYPES = ("*", "*")
    FUNCTION = "reroute"
    CATEGORY = "routing"
    NODE_COLOR = "#FFFF00"  # Yellow color

    def reroute(self, **kwargs):
        return tuple(kwargs.values())

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

NODE_CLASS_MAPPINGS = {
    "YellowBusV2": YellowBusV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "YellowBusV2": "Yellow Bus v2 🚌"
}