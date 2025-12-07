"""Node for concatenating strings in ComfyUI."""

class ConcatString:
    """Node for efficiently concatenating strings with optional additional string."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string_a": ("STRING", {"multiline": True, "default": ""}),
                "string_b": ("STRING", {"multiline": True, "default": ""}),
                "string_c": ("STRING", {"multiline": True, "default": ""}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "concatenate"
    CATEGORY = "klinter"

    def concatenate(self, string_a: str, string_b: str, string_c: str = ""):
        """Efficiently concatenates up to three strings.
        
        Args:
            string_a: First string to concatenate
            string_b: Second string to concatenate
            string_c: Optional third string to concatenate
            
        Returns:
            tuple: Concatenated string
        """
        # Filter out empty strings and join with spaces
        strings = [s for s in (string_a, string_b, string_c) if s]
        result = " ".join(strings)
        return (result,)

# Register the node
NODE_CLASS_MAPPINGS = {
    "concat": ConcatString
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "concat": "Concat String - klinter"
}

# Export the class
__all__ = ['ConcatString']
