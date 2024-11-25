import os
import json

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

    RETURN_TYPES = ("INT", "INT", "STRING")
    RETURN_NAMES = ("width", "height", "name")
    FUNCTION = "return_res"
    CATEGORY = ["image", "utils", "klinter"]
    OUTPUT_NODE = True

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
        selected_info = self.size_dict[size_selected]
        width = int(selected_info["width"])
        height = int(selected_info["height"])
        name = selected_info["name"]
        return (width, height, name)
