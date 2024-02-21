class concat_klinter:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string_a": ("STRING", {"forceInput":True, "default":"", "multiline": True}),
                "string_b": ("STRING", {"forceInput":True, "default":"", "multiline": True}),
                # Assuming string_c remains optional as discussed
                "string_c": ("STRING", {"default":"", "multiline": True}),
            }
        }
    RETURN_TYPES = ("STRING", )
    FUNCTION = "concat"

    CATEGORY = "klinter"

    def concat(self, string_a, string_b, string_c=""):
        # Add a space at the end of each string that is not empty
        string_a_with_space = string_a + " " if string_a else ""
        string_b_with_space = string_b + " " if string_b else ""
        string_c_with_space = string_c + " " if string_c else ""

        # Concatenate the strings
        d = string_a_with_space + string_b_with_space + string_c_with_space
        
        # Optionally, trim the trailing space if you don't want it in the final output
        d = d.rstrip()

        return (d,)


NODE_CLASS_MAPPINGS = {
    "concat_klinter": concat_klinter,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "concat_klinter": "concat string (klitner)",
}
