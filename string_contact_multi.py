"""
String Contact Multi Node
A node that concatenates multiple strings with customizable separators.
Inspired by the multi-input design pattern from Kijai's ComfyUI-KJNodes (https://github.com/kijai/ComfyUI-KJNodes)
"""

from comfy_api.latest import io

class StringContactMulti(io.ComfyNode):
    """A node that allows concatenating multiple strings with a choice of separators."""
    
    @classmethod
    def define_schema(cls) -> io.Schema:
        """Define the schema for the multi-string concatenation node.
        
        Returns:
            io.Schema: Node schema with inputs and outputs
        """
        return io.Schema(
            node_id="string_contact_multi",
            display_name="String Contact Multi - klinter",
            category="string",
            description="Concatenate multiple strings with customizable separators",
            inputs=[
                io.Int.Input("inputcount", default=2, min=2, max=1000, step=1),
                io.Combo.Input("separator", options=["comma", "newline", "pipe", "space"], default="comma"),
            ],
            outputs=[
                io.String.Output()
            ]
        )
    
    @classmethod
    def execute(cls, inputcount, separator, **kwargs) -> io.NodeOutput:
        """Concatenate multiple strings with a customizable separator.
        
        Args:
            inputcount: Number of inputs to concatenate
            separator: Type of separator to use (comma, newline, pipe, or space)
            **kwargs: Dynamic string inputs (string_1, string_2, etc.)
        
        Returns:
            io.NodeOutput: Concatenated string
        """
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
        
        return io.NodeOutput(result)

# Register the node - using lowercase to match __init__.py
NODE_CLASS_MAPPINGS = {
    "string_contact_multi": StringContactMulti
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "string_contact_multi": "String Contact Multi - klinter"
}

# Export the class
__all__ = ['StringContactMulti']
