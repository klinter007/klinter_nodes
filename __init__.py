"""ComfyUI node pack for string manipulation and utilities."""

# Import node classes from individual files
from .concat_string import ConcatString
from .filter_string import FilterString
from .print_floats import PrintFloats
from .yellow_bus_v2 import YellowBusV2
from .zoom_out_composer import ZoomOutComposer
from .folder_loader import FolderLoader
from .extra_padding import ExtraPadding
from .size_selector import SizeSelector
from .load_image_plus import LoadImagePlusKlinter

# Mapping of node identifiers to their respective class implementations
NODE_CLASS_MAPPINGS = {
    # String manipulation nodes
    "concat": ConcatString,  # Keep old name for backward compatibility
    "filter": FilterString,  # Keep old name for backward compatibility
    
    # Utility nodes
    "PrintFloats": PrintFloats,
    "YellowBus": YellowBusV2,  # Keep old name for backward compatibility
    "ZoomOutComposer": ZoomOutComposer,
    "FolderLoader": FolderLoader,
    "ExtraPadding": ExtraPadding,
    "SizeSelector": SizeSelector,
    
    # Image nodes
    "LoadImagePlusKlinter": LoadImagePlusKlinter,
}

# Mapping of node identifiers to their display names for UI or logging purposes
NODE_DISPLAY_NAME_MAPPINGS = {
    # String manipulation nodes
    "concat": "Concat String - klinter",
    "filter": "Filter String - klinter",
    
    # Utility nodes
    "PrintFloats": "Print Floats - klinter",
    "YellowBus": "Yellow Bus v2 🚌 - klinter",
    "ZoomOutComposer": "Zoom Out Composer - klinter",
    "FolderLoader": "Folder Loader - klinter",
    "ExtraPadding": "Extra Padding for Zoom Out - klinter",
    "SizeSelector": "Size Selector - klinter",
    
    # Image nodes
    "LoadImagePlusKlinter": "Load Image Plus - klinter",
}

# Define what symbols this module exports
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# Add this section to specify the location of JavaScript files
WEB_DIRECTORY = "./js"