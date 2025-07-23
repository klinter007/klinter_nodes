import json
import re
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
            json_input: The input string that should contain a valid JSON structure.
            key_to_extract: The key whose value needs to be extracted.

        Returns:
            Tuple[str]: The extracted value.

        Raises:
            ValueError: If JSON is invalid or the key is not found.
        """
        # Step 1: Clean and normalize input
        cleaned_input = json_input.strip()
        
        # Handle common escape sequences
        cleaned_input = cleaned_input.replace('\\n', '\n').replace('\\t', '\t').replace('\\r', '\r')

        # Step 2: Extract JSON-like substring
        start_index = cleaned_input.find('{')
        end_index = cleaned_input.rfind('}')

        if start_index == -1 or end_index == -1 or end_index <= start_index:
            raise ValueError("Could not find a valid JSON object in the input.")

        candidate_json = cleaned_input[start_index:end_index + 1].strip()

        # Step 3: Try to parse JSON directly first
        try:
            data = json.loads(candidate_json)
        except json.JSONDecodeError:
            # If direct parsing fails, try with some common fixes
            try:
                # Replace single quotes with double quotes (common issue)
                fixed_json = candidate_json.replace("'", '"')
                data = json.loads(fixed_json)
            except json.JSONDecodeError:
                # Try parsing as a more lenient JSON-like structure
                try:
                    # Remove trailing commas
                    fixed_json = re.sub(r',(\s*[}\]])', r'\1', candidate_json)
                    data = json.loads(fixed_json)
                except json.JSONDecodeError:
                    # Last resort: fix raw newlines and other control characters in strings
                    try:
                        # Escape raw newlines, tabs, and carriage returns in string values
                        fixed_json = re.sub(r'("(?:[^"\\]|\\.)*")', 
                                          lambda m: m.group(1).replace('\n', '\\n').replace('\t', '\\t').replace('\r', '\\r'), 
                                          candidate_json)
                        data = json.loads(fixed_json)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"Invalid JSON input: {str(e)}")

        # Step 4: Extract the specified key
        if key_to_extract in data:
            value = data[key_to_extract]

            # Return the value as string
            if isinstance(value, str):
                return (value,)
            else:
                # Convert non-string values to JSON string representation
                return (json.dumps(value, ensure_ascii=False),)
        else:
            available_keys = list(data.keys()) if isinstance(data, dict) else []
            raise ValueError(f"Key '{key_to_extract}' not found in JSON structure. Available keys: {available_keys}")

# Node registration
NODE_CLASS_MAPPINGS = {
    "Json Extractor - klinter": JsonExtractorKlinter
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Json Extractor - klinter": "Json Extractor - klinter"
}
