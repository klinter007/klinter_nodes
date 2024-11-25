"""Node for concatenating strings in ComfyUI."""

class ConcatString:
    """Node for efficiently concatenating strings with optional additional string."""

    @classmethod
    def INPUT_TYPES(cls) -> dict:
        """Define the input types for the concatenation operation.
        
        Returns:
            dict: Input type specifications for the node
        """
        return {
            "required": {
                "string_a": ("STRING", {"forceInput": True, "default": "", "multiline": True}),
                "string_b": ("STRING", {"forceInput": True, "default": "", "multiline": True}),
                "string_c": ("STRING", {"default": "", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "concat"
    CATEGORY = ["string", "klinter"]

    def concat(self, string_a: str, string_b: str, string_c: str = "") -> tuple[str]:
        """Efficiently concatenates up to three strings.
        
        Args:
            string_a: First string to concatenate
            string_b: Second string to concatenate
            string_c: Optional third string to concatenate
            
        Returns:
            tuple[str]: Single-element tuple containing the concatenated string
        """
        # Filter out empty strings and join with spaces
        strings = [s for s in (string_a, string_b, string_c) if s]
        return (" ".join(strings),)

# Register the node
NODE_CLASS_MAPPINGS = {
    "concat": ConcatString
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "concat": "Concat String - klinter"
}

# Export the class
__all__ = ['ConcatString']
