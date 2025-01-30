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
        """Extract a specific value from JSON input, ensuring that quoted text remains intact.

        Args:
            json_input: The input string that should contain a valid JSON structure.
            key_to_extract: The key whose value needs to be extracted.

        Returns:
            Tuple[str]: The extracted value with all quoted text preserved.

        Raises:
            ValueError: If JSON is invalid or the key is not found.
        """
        # Step 1: Normalize input (replace '/n' with '\n')
        cleaned_input = json_input.replace('/n', '\n')

        # Step 2: Extract JSON-like substring
        start_index = cleaned_input.find('{')
        end_index = cleaned_input.rfind('}')

        if start_index == -1 or end_index == -1 or end_index <= start_index:
            raise ValueError("Could not find a valid JSON object in the input.")

        candidate_json = cleaned_input[start_index:end_index + 1].strip()

        # Step 3: Parse JSON
        try:
            data = json.loads(candidate_json)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON input: {str(e)}")

        # Step 4: Extract the specified key
        if key_to_extract in data:
            value = data[key_to_extract]

            # Ensure quoted text remains intact
            if isinstance(value, str):
                return (value,)  # Returning it as a raw string keeps quotes intact

            return (json.dumps(value, ensure_ascii=False),)  # If it's a list/dict, return as JSON string

        else:
            raise ValueError(f"Key '{key_to_extract}' not found in JSON structure")

# Node registration
NODE_CLASS_MAPPINGS = {
    "Json Extractor - klinter": JsonExtractorKlinter
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Json Extractor - klinter": "Json Extractor - klinter"
}
