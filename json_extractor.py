"""Node for extracting values from JSON input."""

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

        This node attempts to handle partial or messy JSON by:
        1) Replacing occurrences of '/n' with '\n'.
        2) Searching for the largest substring that looks like JSON.
        3) Extracting the specified key.

        Args:
            json_input: Potentially messy string that should contain JSON.
            key_to_extract: The key to extract from the JSON.

        Returns:
            Tuple[str]: The extracted value.

        Raises:
            ValueError: If JSON is invalid or the key is not found.
        """
        # Step 1: Replace '/n' with '\n' to fix line breaks.
        cleaned_input = json_input.replace('/n', '\n')

        # Step 2: Attempt to find the main JSON portion within the string.
        # We'll look for a substring between the first '{' and the last '}'.
        start_index = cleaned_input.find('{')
        end_index = cleaned_input.rfind('}')

        if start_index == -1 or end_index == -1 or end_index <= start_index:
            raise ValueError("Could not find a valid JSON object in the input.")

        # Extract the candidate JSON substring.
        candidate_json = cleaned_input[start_index:end_index + 1].strip()

        # Now attempt to parse.
        try:
            data = json.loads(candidate_json)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON input: {str(e)}")

        # Step 3: Extract the specified key.
        if key_to_extract in data:
            value = str(data[key_to_extract])
            return (value,)
        else:
            raise ValueError(f"Key '{key_to_extract}' not found in JSON structure")

# Node registration
NODE_CLASS_MAPPINGS = {
    "Json Extractor - klinter": JsonExtractorKlinter
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Json Extractor - klinter": "Json Extractor - klinter"
}
