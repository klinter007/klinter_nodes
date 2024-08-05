# Hack: string type that is always equal in not equal comparisons
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False

# Our any instance wants to be a wildcard string
any = AnyType("*")

class YellowBusV2:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {},
            "optional": {
                f"value_{i}": (any, ) for i in range(1, 11)
            }
        }

    RETURN_TYPES = (any,) * 10
    FUNCTION = "route"
    CATEGORY = "routing"
    NODE_COLOR = "#FFFF00"  # Yellow color

    @classmethod
    def VALIDATE_INPUTS(s, **kwargs):
        return True

    def route(self, **kwargs):
        return tuple(kwargs.values())

NODE_CLASS_MAPPINGS = {
    "YellowBusV2": YellowBusV2
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "YellowBusV2": "Yellow Bus v2 🚌"
}