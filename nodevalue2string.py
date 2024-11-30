"""
Node Value to String Node
A node that converts node values to formatted strings with their node names.
Accepts STRING, INT, and FLOAT inputs.
"""

class NodeValue2String:
    """A node that formats input values with their source node names."""
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "inputcount": ("INT", {"default": 2, "min": 1, "max": 1000, "step": 1}),
                "template": ("STRING", {"default": "{name}:{value}"})
            },
        }
    
    RETURN_TYPES = ("STRING",)
    FUNCTION = "format_node_values"
    CATEGORY = "string"
    
    def format_node_values(self, inputcount, template, **kwargs):
        # Collect and format all connected values
        formatted_strings = []
        for i in range(1, inputcount + 1):
            key = f"value_{i}"
            if key in kwargs and kwargs[key] is not None:
                # Get the value and its type
                value = kwargs[key]
                # Format float values with reasonable precision
                if isinstance(value, float):
                    value = "{:.4f}".format(value)
                # Format using the template
                try:
                    # Note: The actual node name will be handled by the JavaScript
                    # Here we use a placeholder that JS will replace
                    formatted = template.format(name=f"{{node_{i}}}", value=value)
                    formatted_strings.append(formatted)
                except Exception as e:
                    formatted_strings.append(f"Error:{str(e)}")
        
        # Join all formatted strings with newline
        result = "\n".join(formatted_strings)
        
        return (result,)

# Register the node
NODE_CLASS_MAPPINGS = {
    "nodevalue2string": NodeValue2String
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "nodevalue2string": "Node Value to String"
}

# Export the class
__all__ = ['NodeValue2String']
