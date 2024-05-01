import os
import json
import numpy as np
import ast


class concat:
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



class Filter:
    """Class for checking if a given string appears in a list of strings and returning a filter word if true."""

    @classmethod
    def INPUT_TYPES(cls):
        """Defines the input types for the operation."""
        return {
            "required": {
                "in_question": ("STRING", {"forceInput": True, "default": "", "multiline": False}),
                "wordlist": ("STRING", {"forceInput": True, "default": "", "multiline": True}),
                "safeword": ("STRING", {"forceInput": True, "default": "", "multiline": True}),
            }
        }

    RETURN_TYPES = ("STRING",)
    FUNCTION = "Filter"
    CATEGORY = "klinter"

    def Filter(self, in_question, wordlist, safeword):
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
        

class SizeSelector:
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(cls):
        cls.size_sizes, cls.size_dict = cls.read_sizes()
        return {
            'required': {
                'size_selected': (cls.size_sizes,), 
                
            }
        }

    RETURN_TYPES = ( "INT", "INT")
    RETURN_NAMES = ( "width", "height")
    FUNCTION = "return_res"
    OUTPUT_NODE = True
    CATEGORY = "Size"

    @classmethod
    def read_sizes(cls):
        p = os.path.dirname(os.path.realpath(__file__))
        file_path = os.path.join(p, 'sizes.json')
        with open(file_path, 'r') as file:
            data = json.load(file)
        size_sizes = [f"{key} - {value['name']}" for key, value in data['sizes'].items()]
        size_dict = {f"{key} - {value['name']}": value for key, value in data['sizes'].items()}
        return size_sizes, size_dict
  
    def return_res(self, size_selected):
        # Extract resolution name and dimensions using the key
        selected_info = self.size_dict[size_selected]
        width = int(selected_info["width"])
        height = int(selected_info["height"])
        name = selected_info["name"]
        return (width, height, name)

        
    

class SingleString:

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "string": ("STRING", {"default": '', "multiline": True}),
            }
        }
    RETURN_TYPES = ("STRING",)
    FUNCTION = "passtring"

    CATEGORY = "String"

    def passtring(self, string):
        return (string, )

# based on Mikey Nodes
class PrintFloats:
    """Class to convert a float or an array of floats to a string representation, ensuring proper format without extra line breaks."""

    @classmethod
    def INPUT_TYPES(cls):
        return {"required": {"audio_float": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1000000.0, "forceInput": True})}}

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("formatted_float",)
    FUNCTION = "convert"
    CATEGORY = "Utils"  # Simplified category for demonstration

    def convert(self, audio_float):
        # Ensure the correct handling of both single float and arrays of floats
        if isinstance(audio_float, np.ndarray):
            # Process each float in the array and join with a newline
            formatted_float = '\n'.join(f"{x:.2f}" for x in audio_float)
        else:
            # Process a single float
            formatted_float = f"{audio_float:.2f}"

        return (formatted_float,)
    





class ListStringToFloatNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": { "input_data": ("STRING", {"default": "[]"}) },
        }

    RETURN_TYPES = ("FLOAT",)
    RETURN_NAMES = ("output_float",)
    FUNCTION = "process_input"
    CATEGORY = "Custom"

    def process_input(self, input_data):
        # Attempt to evaluate the string input as a list
        try:
            # Convert string to list if it's not a list
            if isinstance(input_data, str):
                input_data = ast.literal_eval(input_data)
            
            # Example operation: calculate the sum of elements if it's a list
            if isinstance(input_data, list):
                result = sum(input_data)
            else:
                result = float(input_data)
        except:
            # Handle errors or unexpected input types
            result = 0.0

        return (result,)
        
class YellowBus:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL", {}),         # Input is a model
                "vae": ("VAE", {}),             # Input is a VAE
                "pos_prompt": ("CONDITIONING", {}),  # Input is a positive prompt (conditioning)
                "neg_prompt": ("CONDITIONING", {}),  # Input is a negative prompt (conditioning)
                "latent": ("LATENT", {}),       # Input is latent embeddings
            }
        }

    RETURN_TYPES = ("MODEL", "VAE", "CONDITIONING", "CONDITIONING", "LATENT")
    RETURN_NAMES = ("model_out", "vae_out", "pos_prompt_out", "neg_prompt_out", "latent_out")
    FUNCTION = "transfer"

    def transfer(self, model, vae, pos_prompt, neg_prompt, latent):
        # Return inputs directly as outputs
        return (model, vae, pos_prompt, neg_prompt, latent)
