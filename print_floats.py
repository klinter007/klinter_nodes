"""Node for formatting float values in ComfyUI."""

import numpy as np

class PrintFloats:
    """Node for converting float or array of floats to string representation."""

    @classmethod
    def INPUT_TYPES(cls) -> dict:
        """Define the input types for float formatting.
        
        Returns:
            dict: Input type specifications for the node
        """
        return {
            "required": {
                "audio_float": ("FLOAT", {
                    "default": 0.0,
                    "min": 0.0,
                    "max": 1000000.0,
                    "forceInput": True
                })
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("formatted_float",)
    FUNCTION = "convert"
    CATEGORY = "utils"

    def convert(self, audio_float: float | np.ndarray) -> tuple[str]:
        """Convert float or array of floats to formatted string.
        
        Args:
            audio_float: Single float or numpy array of floats
            
        Returns:
            tuple[str]: Single-element tuple containing the formatted string
        """
        try:
            if isinstance(audio_float, np.ndarray):
                # Process each float in the array and join with a newline
                formatted_float = '\n'.join(f"{x:.2f}" for x in audio_float)
            else:
                # Process a single float
                formatted_float = f"{audio_float:.2f}"
            return (formatted_float,)
        except Exception as e:
            print(f"Error in float conversion: {str(e)}")
            return ("0.00",)
