"""Dynamic routing node that can handle multiple input/output pairs with adaptive types."""

from comfy_api.latest import io

# Hack: string type that is always equal in not equal comparisons
class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False
    
    def __eq__(self, __value: object) -> bool:
        return True

# Our any instance wants to be a wildcard string
any = AnyType("*")

class YellowBus(io.ComfyNode):
    """A dynamic routing node that can have multiple input/output pairs.
    Each pair automatically adapts its type to match the connected input node.
    """
    
    @classmethod
    def define_schema(cls) -> io.Schema:
        """Define the schema for the yellow bus routing node.
        
        Returns:
            io.Schema: Node schema with inputs and outputs
        """
        return io.Schema(
            node_id="YellowBus",
            display_name="Yellow Bus - klinter",
            category="klinter",
            description="Dynamic routing node with multiple input/output pairs that adapt to connected types",
            inputs=[
                io.Int.Input("pairs", default=2, min=1, max=10, step=1),
                # Dynamic inputs handled via **kwargs in execute
            ],
            outputs=[
                io.Custom("*").Output(display_name=f"out_{i}") for i in range(1, 11)
            ]
        )
    
    @classmethod
    def validate_inputs(cls, **kwargs):
        """All inputs are valid since we handle dynamic types."""
        return True
    
    @classmethod
    def execute(cls, pairs, **kwargs) -> io.NodeOutput:
        """Route inputs to outputs in order.
        Each input maps to its corresponding output with the same type.
        If an input is not connected, its corresponding output will be None.
        """
        # Convert kwargs to list, preserving order and types
        values = []
        for i in range(1, pairs + 1):
            key = f"input_{i}"
            value = kwargs.get(key, None)
            # Store the type information for the UI
            if value is not None:
                value_type = type(value).__name__
            values.append(value)
            
        # Fill remaining outputs with None
        while len(values) < 10:
            values.append(None)
        return io.NodeOutput(*values)

NODE_CLASS_MAPPINGS = {
    "YellowBus": YellowBus
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "YellowBus": "Yellow Bus - klinter"
}
