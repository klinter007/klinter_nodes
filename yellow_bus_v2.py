"""Dynamic routing node that can handle multiple input/output pairs with adaptive types."""

# Define all possible types we might encounter
POSSIBLE_TYPES = ["IMAGE", "LATENT", "MODEL", "CLIP", "VAE", "CONDITIONING", "MASK", "STRING", "INT", "FLOAT"]

class YellowBusV2:
    """A dynamic routing node that can handle multiple input/output pairs.
    The number of pairs is controlled by the inputcount widget.
    Each input is routed to its corresponding output with the same type.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        """Define dynamic inputs. The actual number of inputs is controlled by the UI."""
        return {
            "required": {
                "inputcount": ("INT", {"default": 2, "min": 1, "max": 10, "step": 1}),
            },
            "optional": {
                # Support any type for each input
                f"value_{i}": tuple(POSSIBLE_TYPES) for i in range(1, 11)
            }
        }
    
    # Support any type for each output
    RETURN_TYPES = tuple(POSSIBLE_TYPES)
    RETURN_NAMES = tuple([f"out_{i+1}" for i in range(10)])  # Named outputs for clarity
    FUNCTION = "route"
    CATEGORY = "klinter"
    NODE_COLOR = "#FFFF00"  # Yellow color
    
    @classmethod
    def VALIDATE_INPUTS(s, **kwargs):
        """All inputs are valid since we handle dynamic types."""
        return True
    
    def route(self, inputcount, **kwargs):
        """Route inputs to outputs in order.
        Each input maps to its corresponding output with the same type.
        If an input is not connected, its corresponding output will be None.
        """
        # Convert kwargs to list, preserving order
        values = []
        for i in range(1, inputcount + 1):
            key = f"value_{i}"
            values.append(kwargs.get(key, None))
        # Fill remaining outputs with None
        while len(values) < 10:
            values.append(None)
        return tuple(values)

NODE_CLASS_MAPPINGS = {
    "YellowBus": YellowBusV2  # Match the name in __init__.py
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "YellowBus": "Yellow Bus v2 🚌 - klinter"  # Match the name in __init__.py
}

# Export the class
__all__ = ['YellowBusV2']