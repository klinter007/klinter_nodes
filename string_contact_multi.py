"""
String Contact Multi Node
A node that concatenates multiple strings with customizable separators.
Inspired by the multi-input design pattern from Kijai's ComfyUI-KJNodes (https://github.com/kijai/ComfyUI-KJNodes)
"""

class StringContactMulti:
    """A node that allows concatenating multiple strings with a choice of separators."""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "inputcount": ("INT", {"default": 2, "min": 2, "max": 1000, "step": 1}),
                "separator": (["comma", "newline", "pipe", "space"], {"default": "comma"}),
            },
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "concatenate_strings"
    CATEGORY = "string"
    
    def concatenate_strings(self, inputcount, separator, **kwargs):
        # Define separator mapping
        separator_map = {
            "comma": ",",
            "newline": "\n",
            "pipe": "|",
            "space": " "
        }
        
        # Get the actual separator character
        sep = separator_map[separator]
        
        # Collect all connected strings
        strings = []
        for i in range(1, inputcount + 1):
            key = f"string_{i}"
            if key in kwargs and kwargs[key]:
                strings.append(kwargs[key])
        
        # Join strings with the selected separator
        result = sep.join(strings)
        
        return (result,)

# Register the node - using lowercase to match __init__.py
NODE_CLASS_MAPPINGS = {
    "string_contact_multi": StringContactMulti
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "string_contact_multi": "String Contact Multi - klinter"
}

# Export the class
__all__ = ['StringContactMulti']
