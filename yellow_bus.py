"""Dynamic routing node that can handle multiple input/output pairs with adaptive types."""

# Hack: string type that is always equal in not equal comparisons
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False
    
    def __eq__(self, __value: object) -> bool:
        return True

# Our any instance wants to be a wildcard string
any = AnyType("*")

class YellowBus:
    """A dynamic routing node that can have multiple input/output pairs.
    Each pair automatically adapts its type to match the connected input node.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        """Define dynamic inputs. The actual number of inputs is controlled by the UI."""
        return {
            "required": {
                "pairs": ("INT", {"default": 2, "min": 1, "max": 10, "step": 1}),
            },
            "optional": {
                f"input_{i}": (any,) for i in range(1, 11)  # Support up to 10 pairs
            }
        }
    
    RETURN_TYPES = tuple([any] * 10)  # Support up to 10 outputs
    RETURN_NAMES = tuple([f"out_{i}" for i in range(1, 11)])  # Named outputs for clarity
    FUNCTION = "route"
    CATEGORY = "klinter"
    NODE_COLOR = "#FFFF00"  # Yellow color
    
    @classmethod
    def VALIDATE_INPUTS(s, **kwargs):
        """All inputs are valid since we handle dynamic types."""
        return True
    
    def route(self, pairs, **kwargs):
        """Route inputs to outputs in order.
        Each input maps to its corresponding output with the same type.
        If an input is not connected, its corresponding output will be None.
        """
        # Convert kwargs to list, preserving order
        values = []
        for i in range(1, pairs + 1):
            key = f"input_{i}"
            values.append(kwargs.get(key, None))
        # Fill remaining outputs with None
        while len(values) < 10:
            values.append(None)
        return tuple(values)

NODE_CLASS_MAPPINGS = {
    "YellowBus": YellowBus
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "YellowBus": "Yellow Bus - klinter"
}
