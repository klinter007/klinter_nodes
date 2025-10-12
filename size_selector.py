import os
import json
from comfy_api.latest import io

class SizeSelector(io.ComfyNode):
    _size_sizes = None
    _size_dict = None
    
    @classmethod
    def read_sizes(cls):
        """Read sizes from JSON configuration file.
        
        Returns:
            tuple: List of size options and dictionary mapping options to values
        """
        if cls._size_sizes is None or cls._size_dict is None:
            p = os.path.dirname(os.path.realpath(__file__))
            file_path = os.path.join(p, 'sizes.json')
            with open(file_path, 'r') as file:
                data = json.load(file)
            cls._size_sizes = [f"{key} - {value['name']}" for key, value in data['sizes'].items()]
            cls._size_dict = {f"{key} - {value['name']}": value for key, value in data['sizes'].items()}
        return cls._size_sizes, cls._size_dict
    
    @classmethod
    def define_schema(cls) -> io.Schema:
        """Define the schema for the size selector node.
        
        Returns:
            io.Schema: Node schema with inputs and outputs
        """
        size_options, _ = cls.read_sizes()
        
        return io.Schema(
            node_id="SizeSelector",
            display_name="Size Selector - klinter",
            category="klinter",
            description="Select predefined image dimensions from configuration",
            is_output_node=True,
            inputs=[
                io.Combo.Input("size_selected", options=size_options),
            ],
            outputs=[
                io.Int.Output(display_name="width"),
                io.Int.Output(display_name="height"),
                io.String.Output(display_name="name")
            ]
        )
  
    @classmethod
    def execute(cls, size_selected) -> io.NodeOutput:
        """Return dimensions for selected size.
        
        Args:
            size_selected: Selected size option
            
        Returns:
            io.NodeOutput: Width, height, and name
        """
        _, size_dict = cls.read_sizes()
        selected_info = size_dict[size_selected]
        width = int(selected_info["width"])
        height = int(selected_info["height"])
        name = selected_info["name"]
        return io.NodeOutput(width, height, name)

# Register the node
NODE_CLASS_MAPPINGS = {
    "SizeSelector": SizeSelector
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SizeSelector": "Size Selector - klinter"
}

# Export the class
__all__ = ['SizeSelector']
