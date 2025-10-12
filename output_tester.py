"""Output tester node for debugging and type inspection in ComfyUI."""

import torch
import numpy as np
from PIL import Image
from comfy_api.latest import io

class OutputTester(io.ComfyNode):
    """Node that accepts any input type and reports what it receives for debugging purposes."""

    @classmethod
    def define_schema(cls) -> io.Schema:
        """Define the schema for the output tester node.
        
        Returns:
            io.Schema: Node schema with inputs and outputs
        """
        return io.Schema(
            node_id="OutputTester",
            display_name="Output Tester - klinter",
            category="klinter",
            description="Accept any input type and report details for debugging",
            is_output_node=True,
            inputs=[
                io.Custom("*").Input("input_value"),
                io.Custom("*").Input("optional_input", optional=True),
            ],
            outputs=[
                io.String.Output(display_name="type_info"),
                io.String.Output(display_name="value_info"),
                io.Custom("*").Output(display_name="passthrough")
            ]
        )

    @classmethod
    def execute(cls, input_value, optional_input=None) -> io.NodeOutput:
        """Test and report the type and value of the input.
        
        Args:
            input_value: The primary input value of any type
            optional_input: Optional secondary input for testing
            
        Returns:
            tuple: Type information, value information, and passthrough of the input
        """
        
        # Main input analysis
        type_info = cls._analyze_type(input_value)
        value_info = cls._analyze_value(input_value)
        
        # If optional input is provided, analyze it too
        if optional_input is not None:
            optional_type = cls._analyze_type(optional_input)
            optional_value = cls._analyze_value(optional_input)
            type_info += f"\n\n[Optional Input]\n{optional_type}"
            value_info += f"\n\n[Optional Input]\n{optional_value}"
        
        # Print to console for debugging
        print("\n" + "="*50)
        print("OUTPUT TESTER - Type Analysis")
        print("="*50)
        print(type_info)
        print("-"*50)
        print("OUTPUT TESTER - Value Analysis")
        print("-"*50)
        print(value_info)
        print("="*50 + "\n")
        
        return io.NodeOutput(type_info, value_info, input_value)
    
    @classmethod
    def _analyze_type(cls, value):
        """Analyze and return detailed type information about the value.
        
        Args:
            value: The value to analyze
            
        Returns:
            str: Detailed type information
        """
        info_lines = []
        
        # Basic type information
        value_type = type(value).__name__
        info_lines.append(f"Python Type: {value_type}")
        info_lines.append(f"Module: {type(value).__module__}")
        
        # Check if it's a tensor
        if torch.is_tensor(value):
            info_lines.append(f"Torch Tensor: Yes")
            info_lines.append(f"  - dtype: {value.dtype}")
            info_lines.append(f"  - device: {value.device}")
            info_lines.append(f"  - requires_grad: {value.requires_grad}")
            
            # Likely ComfyUI types based on shape
            if len(value.shape) == 4:
                if value.shape[-1] == 3:
                    info_lines.append(f"  - Likely Type: IMAGE (RGB)")
                elif value.shape[-1] == 4:
                    info_lines.append(f"  - Likely Type: IMAGE (RGBA)")
                else:
                    info_lines.append(f"  - Likely Type: LATENT or Custom Tensor")
            elif len(value.shape) == 3:
                info_lines.append(f"  - Likely Type: MASK or Single Image")
            elif len(value.shape) == 2:
                info_lines.append(f"  - Likely Type: CONDITIONING or 2D Tensor")
        
        # Check if it's a numpy array
        elif isinstance(value, np.ndarray):
            info_lines.append(f"NumPy Array: Yes")
            info_lines.append(f"  - dtype: {value.dtype}")
        
        # Check if it's a PIL Image
        elif isinstance(value, Image.Image):
            info_lines.append(f"PIL Image: Yes")
            info_lines.append(f"  - mode: {value.mode}")
            info_lines.append(f"  - format: {value.format}")
        
        # Check for common ComfyUI types
        elif isinstance(value, dict):
            info_lines.append("Dictionary Keys: " + ", ".join(str(k) for k in value.keys()))
            if 'samples' in value:
                info_lines.append("  - Likely Type: LATENT")
            if 'model' in value:
                info_lines.append("  - Likely Type: MODEL")
            if 'clip' in value:
                info_lines.append("  - Likely Type: CLIP")
        
        # Check if it's a list or tuple
        elif isinstance(value, (list, tuple)):
            info_lines.append(f"Container Type: {value_type}")
            info_lines.append(f"  - Length: {len(value)}")
            if len(value) > 0:
                info_lines.append(f"  - First Element Type: {type(value[0]).__name__}")
                if all(isinstance(item, tuple) and len(item) == 2 for item in value):
                    info_lines.append("  - Likely Type: CONDITIONING")
        
        # String type
        elif isinstance(value, str):
            info_lines.append("String Type: Yes")
        
        # Numeric types
        elif isinstance(value, (int, float, bool)):
            info_lines.append(f"Primitive Type: {value_type}")
        
        return "\n".join(info_lines)
    
    @classmethod
    def _analyze_value(cls, value):
        """Analyze and return information about the value itself.
        
        Args:
            value: The value to analyze
            
        Returns:
            str: Information about the value
        """
        info_lines = []
        
        # Handle tensors
        if torch.is_tensor(value):
            info_lines.append(f"Shape: {list(value.shape)}")
            info_lines.append(f"Min Value: {value.min().item():.4f}")
            info_lines.append(f"Max Value: {value.max().item():.4f}")
            info_lines.append(f"Mean Value: {value.mean().item():.4f}")
            info_lines.append(f"Memory Size: {value.element_size() * value.nelement()} bytes")
        
        # Handle numpy arrays
        elif isinstance(value, np.ndarray):
            info_lines.append(f"Shape: {value.shape}")
            info_lines.append(f"Min Value: {value.min():.4f}")
            info_lines.append(f"Max Value: {value.max():.4f}")
            info_lines.append(f"Mean Value: {value.mean():.4f}")
        
        # Handle PIL Images
        elif isinstance(value, Image.Image):
            info_lines.append(f"Size: {value.size}")
            info_lines.append(f"Mode: {value.mode}")
        
        # Handle dictionaries
        elif isinstance(value, dict):
            info_lines.append(f"Number of Keys: {len(value)}")
            for key, val in value.items():
                if torch.is_tensor(val):
                    info_lines.append(f"  '{key}': Tensor {list(val.shape)}")
                elif isinstance(val, (list, tuple)):
                    info_lines.append(f"  '{key}': {type(val).__name__} (length: {len(val)})")
                else:
                    info_lines.append(f"  '{key}': {type(val).__name__}")
        
        # Handle lists/tuples
        elif isinstance(value, (list, tuple)):
            info_lines.append(f"Length: {len(value)}")
            if len(value) > 0 and len(value) <= 5:
                # Show first few elements for small lists
                for i, item in enumerate(value[:5]):
                    if torch.is_tensor(item):
                        info_lines.append(f"  [{i}]: Tensor {list(item.shape)}")
                    elif isinstance(item, str) and len(item) <= 50:
                        info_lines.append(f"  [{i}]: '{item}'")
                    else:
                        info_lines.append(f"  [{i}]: {type(item).__name__}")
        
        # Handle strings
        elif isinstance(value, str):
            info_lines.append(f"Length: {len(value)} characters")
            if len(value) <= 200:
                info_lines.append(f"Content: '{value}'")
            else:
                info_lines.append(f"Content (truncated): '{value[:100]}...'")
        
        # Handle numeric types
        elif isinstance(value, (int, float)):
            info_lines.append(f"Value: {value}")
        
        elif isinstance(value, bool):
            info_lines.append(f"Value: {value}")
        
        # Handle None
        elif value is None:
            info_lines.append("Value is None")
        
        # Handle unknown types
        else:
            try:
                str_rep = str(value)
                if len(str_rep) <= 200:
                    info_lines.append(f"String Representation: {str_rep}")
                else:
                    info_lines.append(f"String Representation (truncated): {str_rep[:100]}...")
            except:
                info_lines.append("Unable to get string representation")
        
        return "\n".join(info_lines)

# Register the node
NODE_CLASS_MAPPINGS = {
    "OutputTester": OutputTester
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "OutputTester": "Output Tester - klinter"
}

# Export the class
__all__ = ['OutputTester']
