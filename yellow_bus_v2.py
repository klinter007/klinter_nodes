"""Dynamic routing node that can handle multiple input/output pairs with adaptive types."""

# Hack: string type that is always equal in not equal comparisons
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False
    
    def __eq__(self, __value: object) -> bool:
        return True

# Our any instance wants to be a wildcard string
any = AnyType("*")

class YellowBusV2:
    """A dynamic routing node that can have multiple input/output pairs.
    Each pair automatically adapts its type to match the connected input node.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        """Define dynamic inputs. The actual number of inputs is controlled by the UI."""
        return {
            "required": {},
            "optional": {
                f"value_{i}": (any,) for i in range(1, 11)  # Support up to 10 pairs
            }
        }
    
    RETURN_TYPES = tuple([any] * 10)  # Support up to 10 outputs
    RETURN_NAMES = tuple([f"out_{i+1}" for i in range(10)])  # Named outputs for clarity
    FUNCTION = "route"
    # List multiple categories to make the node appear in both
    CATEGORY = ["routing", "utils", "klinter"]
    NODE_COLOR = "#FFFF00"  # Yellow color

    @classmethod
    def VALIDATE_INPUTS(s, **kwargs):
        """All inputs are valid since we handle dynamic types."""
        return True

    def route(self, **kwargs):
        """Route inputs to outputs in order.
        If an input is not connected, its corresponding output will be None.
        """
        # Convert kwargs to list, preserving order
        values = []
        for i in range(1, 11):
            key = f"value_{i}"
            values.append(kwargs.get(key, None))
        return tuple(values)

NODE_CLASS_MAPPINGS = {
    "YellowBusV2": YellowBusV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "YellowBusV2": "Yellow Bus v2 🚌"
}

# Export the class
__all__ = ['YellowBusV2']