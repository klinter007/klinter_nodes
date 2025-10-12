import random
from comfy_api.latest import io

class AspectSelector(io.ComfyNode):
    # Base ratios and their relative proportions
    BASE_RATIOS = {
        "1:1": (1.0, 1.0),
        "---": "---",
        "3:2": (1.5, 1.0),
        "5:4": (1.25, 1.0),
        "8:5": (1.6, 1.0),
        "16:9": (1.7778, 1.0),
        "21:9": (2.3333, 1.0),
        "---": "---",
        "2:3": (1.0, 1.5),
        "4:5": (1.0, 1.25),
        "5:8": (1.0, 1.6),
        "9:16": (1.0, 1.7778),
        "9:21": (1.0, 2.3333),
    }

    BASE_SIZES = {
        "512": 512,
        "768": 768,
        "1024": 1024,
        "1152": 1152,
        "1280": 1280,
        "1408": 1408,
        "1536": 1536
    }
    
    @classmethod
    def get_dimensions(cls, base_size, ratio):
        """Calculate dimensions for given base size and ratio.
        
        Args:
            base_size: Selected base resolution key
            ratio: Selected aspect ratio key
            
        Returns:
            dict: Dictionary with width and height, or None if invalid
        """
        if ratio == "---":
            return None
            
        base = cls.BASE_SIZES[base_size]
        width_mult, height_mult = cls.BASE_RATIOS[ratio]
        
        # Calculate dimensions while maintaining the base size as the smaller dimension
        if width_mult >= height_mult:
            height = base
            width = int(base * width_mult / height_mult)
        else:
            width = base
            height = int(base * height_mult / width_mult)
            
        # Ensure dimensions are even numbers
        width = width if width % 2 == 0 else width + 1
        height = height if height % 2 == 0 else height + 1
        
        return {
            "width": width,
            "height": height
        }
    
    @classmethod
    def define_schema(cls) -> io.Schema:
        """Define the schema for the aspect selector node.
        
        Returns:
            io.Schema: Node schema with inputs and outputs
        """
        return io.Schema(
            node_id="AspectSelector",
            display_name="Aspect Ratio Selector - klinter",
            category="klinter",
            description="Select aspect ratio and base resolution to calculate dimensions",
            is_output_node=True,
            inputs=[
                io.Combo.Input("base_resolution", options=list(cls.BASE_SIZES.keys()), default="1536"),
                io.Combo.Input("aspect_ratio", options=list(cls.BASE_RATIOS.keys())),
                io.Int.Input("seed", default=0, min=0, max=0xffffffffffffffff),
            ],
            outputs=[
                io.Int.Output(display_name="width"),
                io.Int.Output(display_name="height"),
                io.String.Output(display_name="name")
            ]
        )

    @classmethod
    def execute(cls, base_resolution, aspect_ratio, seed) -> io.NodeOutput:
        """Calculate and return dimensions based on aspect ratio selection.
        
        Args:
            base_resolution: Selected base resolution
            aspect_ratio: Selected aspect ratio (or randomized if seed != 0)
            seed: Random seed for ratio selection (0 = no randomization)
            
        Returns:
            io.NodeOutput: Width, height, and aspect ratio name
        """
        # If seed is not 0, use it to randomly select an aspect ratio
        if seed != 0:
            random.seed(seed)
            valid_ratios = [ratio for ratio in cls.BASE_RATIOS.keys() if ratio != "---"]
            aspect_ratio = random.choice(valid_ratios)
        
        # Calculate dimensions based on selected base resolution and ratio
        selected_info = cls.get_dimensions(base_resolution, aspect_ratio)
        if selected_info is None:
            return io.NodeOutput(0, 0, "invalid")
            
        width = selected_info["width"]
        height = selected_info["height"]
        return io.NodeOutput(width, height, aspect_ratio)

# Register the node
NODE_CLASS_MAPPINGS = {
    "AspectSelector": AspectSelector
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AspectSelector": "Aspect Ratio Selector - klinter"
}