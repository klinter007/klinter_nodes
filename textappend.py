import os
import folder_paths

class TextAppendNode:
    def __init__(self):
        self.output_dir = folder_paths.get_output_directory()
        self.type = "output"

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"multiline": True}),
                "filename": ("STRING", {"default": "output.txt"})
            },
        }

    RETURN_TYPES = ()
    FUNCTION = "append_text"
    OUTPUT_NODE = True

    CATEGORY = "text"

    def append_text(self, text, filename):
        full_path = os.path.join(self.output_dir, filename)
        
        # Ensure the directory exists
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        
        # Append the text to the file
        with open(full_path, 'a', encoding='utf-8') as file:
            file.write(text + '\n')
        
        print(f"Text appended to {full_path}")
        return ()

NODE_CLASS_MAPPINGS = {
    "TextAppendNode": TextAppendNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "TextAppendNode": "Append Text to File"
}