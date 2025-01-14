"""Node for extracting values from JSON input."""

import json
from typing import Dict, Any, Tuple

class JsonExtractorKlinter:
    """Node that extracts a specified value from JSON input."""
    
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls) -> Dict[str, Any]:
        return {
            "required": {
                "json_input": ("STRING", {"multiline": True}),
                "key_to_extract": ("STRING", {"default": "enhanced_prompt"})
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "extract_json_value"
    CATEGORY = "utils/json"

    def extract_json_value(self, json_input: str, key_to_extract: str) -> Tuple[str]:
        """Extract a specific value from JSON input.
        
        Args:
            json_input: JSON formatted string input
            key_to_extract: The key to extract from the JSON
            
        Returns:
            Tuple containing the extracted value as string
            
        Raises:
            ValueError: If JSON is invalid or key is not found
        """
        try:
            # Parse the JSON input
            data = json.loads(json_input)
            
            # Extract the specified key
            if key_to_extract in data:
                value = str(data[key_to_extract])  # Convert to string to handle various types
                return (value,)  # Return as tuple for ComfyUI
            else:
                raise ValueError(f"No '{key_to_extract}' field found in JSON input")
                
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON input")
        except Exception as e:
            raise ValueError(f"Error processing input: {str(e)}")

# Node registration
NODE_CLASS_MAPPINGS = {
    "Json Extractor - klinter": JsonExtractorKlinter
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Json Extractor - klinter": "Json Extractor - klinter"
}
