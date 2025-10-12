import os
import io
import json
import random
import folder_paths
from comfy_extras.nodes_audio import SaveAudio
from comfy_api.latest import io as comfy_io

class SaveAudioPlus(comfy_io.ComfyNode, SaveAudio):
    """
    Enhanced version of SaveAudio node with playback functionality.
    """
    
    @classmethod
    def define_schema(cls) -> comfy_io.Schema:
        """Define the schema for the save audio plus node.
        
        Returns:
            comfy_io.Schema: Node schema with inputs and outputs
        """
        return comfy_io.Schema(
            node_id="SaveAudioPlus",
            display_name="Save Audio+ - Klinter",
            category="audio",
            description="Enhanced version of SaveAudio with playback functionality",
            is_output_node=True,
            inputs=[
                comfy_io.Custom("AUDIO").Input("audio"),
                comfy_io.String.Input("filename_prefix", default="audio/ComfyUI"),
            ],
            outputs=[]
        )

    @classmethod
    def execute(cls, audio, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None):
        # Call parent class to save the audio and get the results
        # Need to create an instance for parent method call since it's not a classmethod
        instance = SaveAudio()
        results = instance.save_audio(audio, filename_prefix, prompt, extra_pnginfo)
        
        # Return the results wrapped in NodeOutput
        # This will automatically trigger audio playback in the UI
        if results:
            return comfy_io.NodeOutput(*results) if isinstance(results, tuple) else comfy_io.NodeOutput(results)
        return comfy_io.NodeOutput()

# Register the node
NODE_CLASS_MAPPINGS = {
    "SaveAudioPlus": SaveAudioPlus
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveAudioPlus": "Save Audio+"
}
