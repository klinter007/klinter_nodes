"""Node for filtering strings based on a wordlist in ComfyUI."""

class FilterString:
    """Node for checking if a given string appears in a list of strings and returning a filter word if true."""

    @classmethod
    def INPUT_TYPES(cls) -> dict:
        """Define the input types for the filtering operation.
        
        Returns:
            dict: Input type specifications for the node
        """
        return {
            "required": {
                "in_question": ("STRING", {"forceInput": True, "default": "", "multiline": False}),
                "wordlist": ("STRING", {"forceInput": True, "default": "", "multiline": True}),
                "safeword": ("STRING", {"forceInput": True, "default": "", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "filter_string"
    CATEGORY = ["string", "klinter"]

    def filter_string(self, in_question: str, wordlist: str, safeword: str) -> tuple[str]:
        """Check if a string exists in a wordlist and return either the safeword or original string.
        
        Args:
            in_question: The string to search for
            wordlist: Space-separated list of words to search in
            safeword: Word to return if in_question is found in wordlist
            
        Returns:
            tuple[str]: Either safeword or in_question depending on if in_question is in wordlist
        """
        try:
            # Convert the wordlist string into a list of words
            words = wordlist.split()
            
            # Check if in_question is in the list of words
            return (safeword,) if in_question in words else (in_question,)
        except Exception as e:
            print(f"Error in filter_string: {str(e)}")
            return (in_question,)

# Register the node
NODE_CLASS_MAPPINGS = {
    "filter": FilterString
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "filter": "Filter String - klinter"
}

# Export the class
__all__ = ['FilterString']
