"""ComfyUI node pack for string manipulation and utilities - V3 Schema."""

from comfy_api.latest import ComfyExtension, io

# Import node classes from individual files
from .concat_string import ConcatString
from .filter_string import FilterString
from .yellow_bus import YellowBus
from .zoom_out_composer import ZoomOutComposer
from .folder_loader import FolderLoader
from .size_selector import SizeSelector
from .load_image_plus import LoadImagePlusKlinter
from .aspect_selector import AspectSelector
from .speed_ramp import SpeedRampNode
from .string_contact_multi import StringContactMulti
from .node_value_to_string import NodeValue2StringMulti
from .outpaint_padding import OutpaintPadding
from .video_extend import LoadVideoForExtending, PrepVideoForExtend
from .video_from_folder import VideoFromFolder
from .nano_banana_multi_input import NanoBananaMultiInput
from .json_extractor import JsonExtractorKlinter
from .save_audio_plus import SaveAudioPlus
from .bbox_cropper import BBoxCropper
from .output_tester import OutputTester
from .flexible_batch_image import FlexibleBatchImage

class KlinterNodesExtension(ComfyExtension):
    """Extension providing custom nodes for ComfyUI."""
    
    async def get_node_list(self) -> list[type[io.ComfyNode]]:
        """Return list of all nodes provided by this extension.
        
        Returns:
            list: All ComfyNode classes in this extension
        """
        return [
            # String manipulation nodes
            ConcatString,
            FilterString,
            StringContactMulti,
            NodeValue2StringMulti,
            
            # Core utility nodes
            YellowBus,
            
            # Image processing nodes
            ZoomOutComposer,
            FolderLoader,
            SizeSelector,
            LoadImagePlusKlinter,
            AspectSelector,
            OutpaintPadding,
            BBoxCropper,
            FlexibleBatchImage,
            
            # Video processing nodes
            LoadVideoForExtending,
            PrepVideoForExtend,
            VideoFromFolder,
            SpeedRampNode,
            
            # AI Image Generation nodes
            NanoBananaMultiInput,
            
            # JSON processing nodes
            JsonExtractorKlinter,
            
            # Audio processing nodes
            SaveAudioPlus,
            
            # Debug and testing nodes
            OutputTester,
        ]

async def comfy_entrypoint() -> KlinterNodesExtension:
    """ComfyUI V3 entry point for registering nodes.
    
    Returns:
        KlinterNodesExtension: Extension instance with all nodes
    """
    return KlinterNodesExtension()

# Add this section to specify the location of JavaScript files
WEB_DIRECTORY = "./js"

# List of JavaScript files to include
WEB_EXTENSIONS = [
    "yellow_bus.js",
    "expandable_yellow_bus.js",
    "queue_counter_logic.js",
    "queue_counter_ui.js",
    "node_to_string.js",
    "nodevalue2string.js",
    "string_contact_multi.js",
    "video_upload.js"
]

# Define what symbols this module exports
__all__ = ['comfy_entrypoint', 'KlinterNodesExtension', 'WEB_DIRECTORY', 'WEB_EXTENSIONS']
