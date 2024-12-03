"""
Node Value to String Multi Node
A node that converts multiple node values to formatted strings with their node names.
Accepts STRING, INT, and FLOAT inputs.
"""

class NodeValue2StringMulti:
    """A node that formats multiple input values with their source node names."""
    
    TEMPLATE = "{name}:{value}"
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "inputcount": ("INT", {"default": 2, "min": 1, "max": 1000, "step": 1}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "format_node_values"
    CATEGORY = "string"
    OUTPUT_NODE = True

    def get_node_title(self, value):
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

    def get_node_value(self, value):
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

    def format_node_values(self, inputcount, **kwargs):
        """
        Format node values with their source node names.
        
        Args:
            inputcount (int): Number of inputs to process
            **kwargs: Dynamic input values
        
        Returns:
            tuple: Formatted string result
        """
        # Collect and format all connected values
        formatted_strings = []
        
        # Process inputs in order from value_1 to value_N
        for i in range(1, inputcount + 1):
            key = f"value_{i}"
            
            if key in kwargs and kwargs[key] is not None:
                value = kwargs[key]
                
                # Get node title for the input
                node_title = self.get_node_title(value)
                
                # Format the value
                formatted_value = self.get_node_value(value)
                
                # Create formatted string
                try:
                    formatted = self.TEMPLATE.format(name=node_title, value=formatted_value)
                    formatted_strings.append(formatted)
                except Exception as e:
                    formatted_strings.append(f"Error formatting input {i}: {str(e)}")
        
        # Join all formatted strings with newline
        result = "\n".join(formatted_strings)
        return (result,)

# Register the node
NODE_CLASS_MAPPINGS = {
    "nodevalue2stringmulti": NodeValue2StringMulti
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "nodevalue2stringmulti": "Node Value to String Multi - klinter"
}

# Export the class
__all__ = ['NodeValue2StringMulti']
