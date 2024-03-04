class concat_klinter:
    """Class for concatenating strings with optional additional string, following klinter guidelines."""

    @classmethod
    def INPUT_TYPES(cls):
        """Defines the input types for the concatenation operation."""
        return {
            "required": {
                "string_a": ("STRING", {"forceInput": True, "default": "", "multiline": True}),
                "string_b": ("STRING", {"forceInput": True, "default": "", "multiline": True}),
                # Assuming string_c remains optional as indicated
                "string_c": ("STRING", {"default": "", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "concat"
    CATEGORY = "klinter"

    def concat(self, string_a, string_b, string_c=""):
        """Concatenates up to three strings, adding a space between non-empty strings."""
        # Ensure each non-empty string ends with a space for proper concatenation
        string_a_with_space = f"{string_a} " if string_a else ""
        string_b_with_space = f"{string_b} " if string_b else ""
        string_c_with_space = f"{string_c} " if string_c else ""

        # Concatenate the strings and remove any trailing space
        concatenated_string = (string_a_with_space + string_b_with_space + string_c_with_space).rstrip()

        return (concatenated_string,)






class whitelist:
    """Class for checking if a given string appears in a list of strings and returning a filter word if true."""

    @classmethod
    def INPUT_TYPES(cls):
        """Defines the input types for the operation."""
        return {
            "required": {
                "in_question": ("STRING", {"forceInput": True, "default": "", "multiline": True}),
                "wordlist": ("STRING", {"forceInput": True, "default": "", "multiline": True}),
                "safeword": ("STRING", {"forceInput": True, "default": "", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "whitelist"
    CATEGORY = "klinter"

    def whitelist(self, in_question, wordlist, safeword):
        """
        Checks if 'in_question' exists within 'wordlist'. If it does, returns 'safeword',
        otherwise returns 'in_question'.
        
        Args:
            in_question (str): The string to search for.
            wordlist (str): A string containing a list of words, assumed to be space-separated.
            safeword (str): The word to return if 'in_question' is found in 'wordlist'.
        
        Returns:
            str: 'safeword' if 'in_question' is found in 'wordlist', else 'in_question'.
        """
        # Convert the 'wordlist' string into a list of words
        words = wordlist.split()
        
        # Check if 'in_question' is in the list of words
        if in_question in words:
            return (safeword,)
        else:
            return (in_question,)


class PresentString:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "text": ("STRING", {"forceInput": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "PresentString"
    OUTPUT_NODE = True

    CATEGORY = "klinter"

    def PresentString(self, text):
        # Parse the string
        return {"ui": {"text": text}, "result": (text,)}


# Mapping of this node class for easy reference or extension
NODE_CLASS_MAPPINGS = {
    "whitelist": whitelist,
    "concat_klinter": concat_klinter,
    "PresentString": PresentString,
}



# Mapping of node identifier to its display name for UI or logging purposes
NODE_DISPLAY_NAME_MAPPINGS = {
    "whitelist": "whitelist (Klinter)",
    "concat_klinter": "Concat String (Klinter)",
    "PresentString": "Show String (klinter)",
}
