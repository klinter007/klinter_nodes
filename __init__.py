"""ComfyUI node pack for string manipulation and utilities."""

# Import node classes from individual files
from .concat_string import ConcatString
from .filter_string import FilterString
from .yellow_bus import YellowBus
from .zoom_out_composer import ZoomOutComposer
from .folder_loader import FolderLoader
from .extra_padding import ExtraPadding
from .size_selector import SizeSelector
from .load_image_plus import LoadImagePlusKlinter

# Mapping of node identifiers to their respective class implementations
NODE_CLASS_MAPPINGS = {
    # String manipulation nodes
    "concat": ConcatString,
    "filter": FilterString,
    
    # Core nodes
    "YellowBus": YellowBus,
    
    # Image processing nodes
    "ZoomOutComposer": ZoomOutComposer,
    "FolderLoader": FolderLoader,
    "ExtraPadding": ExtraPadding,
    "SizeSelector": SizeSelector,
    "LoadImagePlus": LoadImagePlusKlinter,
}

# Mapping of node identifiers to their display names for UI or logging purposes
NODE_DISPLAY_NAME_MAPPINGS = {
    # String manipulation nodes
    "concat": "Concat String - klinter",
    "filter": "Filter String - klinter",
    
    # Core nodes
    "YellowBus": "Yellow Bus - klinter",
    
    # Image processing nodes
    "ZoomOutComposer": "Zoom Out Composer - klinter",
    "FolderLoader": "Folder Loader - klinter",
    "ExtraPadding": "Extra Padding for Zoom Out - klinter",
    "SizeSelector": "Size Selector - klinter",
    "LoadImagePlus": "Load Image Plus - klinter",
}

# Define what symbols this module exports
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# Add this section to specify the location of JavaScript files
WEB_DIRECTORY = "./js"