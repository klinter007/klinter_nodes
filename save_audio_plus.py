import os
import io
import json
import random
import folder_paths
from comfy_extras.nodes_audio import SaveAudio

class SaveAudioPlus:
    """
    Enhanced version of SaveAudio node with playback functionality.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "audio": ("AUDIO", ),
                "filename_prefix": ("STRING", {"default": "audio/ComfyUI"})
            },
            "hidden": {
                "prompt": "PROMPT", 
                "extra_pnginfo": "EXTRA_PNGINFO"
            }
        }

    RETURN_TYPES = ()
    FUNCTION = "save_audio"
    OUTPUT_NODE = True
    CATEGORY = "audio"

    def save_audio(self, audio, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None):
        # Use composition - create SaveAudio instance and delegate to it
        save_audio_node = SaveAudio()
        return save_audio_node.save_audio(audio, filename_prefix, prompt, extra_pnginfo)

# Register the node
NODE_CLASS_MAPPINGS = {
    "SaveAudioPlus": SaveAudioPlus
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveAudioPlus": "Save Audio+"
}
