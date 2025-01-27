import os
import io
import json
import random
import folder_paths
from comfy_extras.nodes_audio import SaveAudio

class SaveAudioPlus(SaveAudio):
    """
    Enhanced version of SaveAudio node with playback functionality.
    """
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                "audio": ("AUDIO",),
                "filename_prefix": ("STRING", {"default": "audio/ComfyUI"})
            },
            "hidden": {"prompt": "PROMPT", "extra_pnginfo": "EXTRA_PNGINFO"},
        }

    RETURN_TYPES = ()
    FUNCTION = "save_audio"
    OUTPUT_NODE = True
    CATEGORY = "audio"

    def save_audio(self, audio, filename_prefix="ComfyUI", prompt=None, extra_pnginfo=None):
        # Call parent class to save the audio and get the results
        results = super().save_audio(audio, filename_prefix, prompt, extra_pnginfo)
        
        # Return the results directly - they're already in the correct format
        # This will automatically trigger audio playback in the UI
        return results

# Register the node
NODE_CLASS_MAPPINGS = {
    "SaveAudioPlus": SaveAudioPlus
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "SaveAudioPlus": "Save Audio+"
}
