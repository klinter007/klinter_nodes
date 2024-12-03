"""
Node Value to String Nodes
Provides both multi-input and single-input nodes for converting node values to formatted strings.
"""

class NodeValue2StringBase:
    """Base class for node value to string conversion."""
    
    TEMPLATE = "{name}:{value}"
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


class NodeValue2StringMulti(NodeValue2StringBase):
    """A node that formats multiple input values with their source node names."""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "inputcount": ("INT", {"default": 2, "min": 1, "max": 1000, "step": 1}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "format_node_values"

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


class NodeValue2String(NodeValue2StringBase):
    """A node that formats a single input value with its source node name."""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "value": ("*",),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "format_node_value"

    def format_node_value(self, value):
        """
        Format a single node value with its source node name.
        
        Args:
            value: Input value to format
        
        Returns:
            tuple: Formatted string result
        """
        # Get node title for the input
        node_title = self.get_node_title(value)
        
        # Format the value
        formatted_value = self.get_node_value(value)
        
        # Create formatted string
        try:
            result = self.TEMPLATE.format(name=node_title, value=formatted_value)
            return (result,)
        except Exception as e:
            return (f"Error formatting input: {str(e)}",)


# Register the nodes
NODE_CLASS_MAPPINGS = {
    "nodevalue2stringmulti": NodeValue2StringMulti,
    "nodevalue2string": NodeValue2String
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "nodevalue2stringmulti": "Node Value to String Multi - klinter",
    "nodevalue2string": "Node Value to String - klinter"
}

# Export the classes
__all__ = ['NodeValue2StringMulti', 'NodeValue2String']
