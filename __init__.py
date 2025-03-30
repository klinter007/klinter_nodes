"""ComfyUI node pack for string manipulation and utilities."""

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
from .json_extractor import JsonExtractorKlinter
from .save_audio_plus import SaveAudioPlus
from .bbox_cropper import BBoxCropper

# Mapping of node identifiers to their respective class implementations
NODE_CLASS_MAPPINGS = {
    # String manipulation nodes
    "concat": ConcatString,
    "filter": FilterString,
    "string_contact_multi": StringContactMulti,
    "nodevalue2stringmulti": NodeValue2StringMulti,
    
    # Core nodes
    "YellowBus": YellowBus,
    
    # Image processing nodes
    "ZoomOutComposer": ZoomOutComposer,
    "FolderLoader": FolderLoader,
    "SizeSelector": SizeSelector,
    "LoadImagePlus": LoadImagePlusKlinter,
    "AspectSelector": AspectSelector,
    "SpeedRamp": SpeedRampNode,
    "OutpaintPadding": OutpaintPadding,
    "BBoxCropper": BBoxCropper,
    
    # Video processing nodes
    "LoadVideoForExtendingKlinter": LoadVideoForExtending,
    "PrepVideoForExtendKlinter": PrepVideoForExtend,
    
    # JSON processing nodes
    "Json Extractor - klinter": JsonExtractorKlinter,
    
    # Audio processing nodes
    "SaveAudioPlus": SaveAudioPlus
}

# Mapping of node identifiers to their display names for UI or logging purposes
NODE_DISPLAY_NAME_MAPPINGS = {
    # String manipulation nodes
    "concat": "Concat String - klinter",
    "filter": "Filter String - klinter",
    "string_contact_multi": "String Contact Multi - klinter",
    "nodevalue2stringmulti": "Node Value to String Multi - klinter",
    
    # Core nodes
    "YellowBus": "Yellow Bus - klinter",
    
    # Image processing nodes
    "ZoomOutComposer": "Zoom Out Composer - klinter",
    "FolderLoader": "Folder Loader - klinter",
    "SizeSelector": "Size Selector - klinter",
    "LoadImagePlus": "Load Image Plus - klinter",
    "AspectSelector": "Aspect Selector - klinter",
    "SpeedRamp": "Speed Ramp - klinter",
    "OutpaintPadding": "Outpaint Padding - Klinter",
    "BBoxCropper": "BBox Cropper - klinter",
    
    # Video processing nodes
    "LoadVideoForExtendingKlinter": "Load Video For Extending - Klinter",
    "PrepVideoForExtendKlinter": "Prep Video For Extend - Klinter",
    
    # JSON processing nodes
    "Json Extractor - klinter": "Json Extractor - klinter",
    
    # Audio processing nodes
    "SaveAudioPlus": "Save Audio+ - Klinter"
}

# Define what symbols this module exports
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

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