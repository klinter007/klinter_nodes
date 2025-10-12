"""
Node Value to String Nodes
Provides both multi-input and single-input nodes for converting node values to formatted strings.
"""

from comfy_api.latest import io

class NodeValue2StringBase:
    """Base class for node value to string conversion."""
    
    TEMPLATE = "{name}:{value}"

    @classmethod
    def get_node_title(cls, value):
        """
        Attempt to extract the node's title or type from the input value.
        
        Args:
            value: Input value to extract node information from
        
        Returns:
            str: Node title or type
        """
        try:
            # Check if the value has metadata with node information
            if hasattr(value, '_meta'):
                # Try to get node title or type from metadata
                node_title = value._meta.get('node_title')
                node_type = value._meta.get('node_type')
                
                if node_title:
                    return node_title
                elif node_type:
                    return node_type
            
            # Fallback to checking the value's class name
            return value.__class__.__name__
        
        except Exception:
            # If all else fails, return a generic name
            return "Unknown Node"

    @classmethod
    def get_node_value(cls, value):
        """
        Format different types of values consistently.
        
        Args:
            value: Input value to format
        
        Returns:
            str: Formatted value string
        """
        # Handle different value types
        if value is None:
            return "None"
        elif isinstance(value, float):
            return f"{value:.4f}"
        elif isinstance(value, list):
            # For list types, return first element or list length
            return str(value[0]) if value else "[]"
        else:
            return str(value)


class NodeValue2StringMulti(io.ComfyNode, NodeValue2StringBase):
    """A node that formats multiple input values with their source node names."""
    
    @classmethod
    def define_schema(cls) -> io.Schema:
        """Define the schema for the node value to string multi node.
        
        Returns:
            io.Schema: Node schema with inputs and outputs
        """
        return io.Schema(
            node_id="nodevalue2stringmulti",
            display_name="Node Value to String Multi - klinter",
            category="string",
            description="Format multiple input values with their source node names",
            is_output_node=True,
            inputs=[
                io.Int.Input("inputcount", default=2, min=1, max=1000, step=1),
            ],
            outputs=[
                io.String.Output()
            ]
        )

    @classmethod
    def execute(cls, inputcount, **kwargs) -> io.NodeOutput:
        """
        Format node values with their source node names.
        
        Args:
            inputcount (int): Number of inputs to process
            **kwargs: Dynamic input values
        
        Returns:
            io.NodeOutput: Formatted string result
        """
        # Collect and format all connected values
        formatted_strings = []
        
        # Process inputs in order from value_1 to value_N
        for i in range(1, inputcount + 1):
            key = f"value_{i}"
            
            if key in kwargs and kwargs[key] is not None:
                value = kwargs[key]
                
                # Get node title for the input
                node_title = cls.get_node_title(value)
                
                # Format the value
                formatted_value = cls.get_node_value(value)
                
                # Create formatted string
                try:
                    formatted = cls.TEMPLATE.format(name=node_title, value=formatted_value)
                    formatted_strings.append(formatted)
                except Exception as e:
                    formatted_strings.append(f"Error formatting input {i}: {str(e)}")
        
        # Join all formatted strings with newline
        result = "\n".join(formatted_strings)
        return io.NodeOutput(result)


# Register the nodes
NODE_CLASS_MAPPINGS = {
    "nodevalue2stringmulti": NodeValue2StringMulti
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "nodevalue2stringmulti": "Node Value to String Multi - klinter"
}

# Export the classes
__all__ = ['NodeValue2StringMulti']
