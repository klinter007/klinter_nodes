"""Node for concatenating strings in ComfyUI."""

from comfy_api.latest import io

class ConcatString(io.ComfyNode):
    """Node for efficiently concatenating strings with optional additional string."""

    @classmethod
    def define_schema(cls) -> io.Schema:
        """Define the schema for the concatenation node.
        
        Returns:
            io.Schema: Node schema with inputs and outputs
        """
        return io.Schema(
            node_id="concat",
            display_name="Concat String - klinter",
            category="klinter",
            description="Efficiently concatenates up to three strings",
            inputs=[
                io.String.Input("string_a", default="", multiline=True, force_input=True),
                io.String.Input("string_b", default="", multiline=True, force_input=True),
                io.String.Input("string_c", default="", multiline=True),
            ],
            outputs=[
                io.String.Output()
            ]
        )

    @classmethod
    def execute(cls, string_a: str, string_b: str, string_c: str = "") -> io.NodeOutput:
        """Efficiently concatenates up to three strings.
        
        Args:
            string_a: First string to concatenate
            string_b: Second string to concatenate
            string_c: Optional third string to concatenate
            
        Returns:
            io.NodeOutput: Concatenated string
        """
        # Filter out empty strings and join with spaces
        strings = [s for s in (string_a, string_b, string_c) if s]
        result = " ".join(strings)
        return io.NodeOutput(result)

# Register the node
NODE_CLASS_MAPPINGS = {
    "concat": ConcatString
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "concat": "Concat String - klinter"
}

# Export the class
__all__ = ['ConcatString']
