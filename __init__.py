# Import local node class modules
from .nodes import concat, Filter, PresentString, SizeSelector, SingleString, YellowBus, Florence2Captions2IPA
from .yellow_bus_v2 import YellowBusV2
from .zoom_out_composer import ZoomOutComposer
from .folder_loader import FolderLoader
from .extra_padding import ExtraPadding

# Mapping of node identifiers to their respective class implementations
NODE_CLASS_MAPPINGS = {
    "concat": concat,
    "Filter": Filter,
    "PresentString": PresentString,
    "SizeSelector": SizeSelector,
    "SingleString": SingleString,
    "YellowBus": YellowBus,
    "Florence2Captions2IPA": Florence2Captions2IPA,
    "YellowBusV2": YellowBusV2,
    "ZoomOutComposer": ZoomOutComposer,
    "FolderLoader": FolderLoader,
    "ExtraPadding": ExtraPadding,
}

# Mapping of node identifiers to their display names for UI or logging purposes
NODE_DISPLAY_NAME_MAPPINGS = {
    "concat": "Concat String (Klinter)",
    "Filter": "Filter (Klinter)",
    "PresentString": "Show String (klinter)",
    "SizeSelector": "Size Selector (klinter)",
    "SingleString": "Single String (klinter)",
    "YellowBus": "YellowBus (klinter)",
    "Florence2Captions2IPA": "Florence2Captions2IPA (klinter)",
    "YellowBusV2": "Yellow Bus v2 (klinter)",
    "ZoomOutComposer": "Zoom Out Composer (klinter)",
    "FolderLoader": "Folder Loader (klinter)",
    "ExtraPadding": "Extra Padding (klinter)",
}

# Define what symbols this module exports
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']

# Add this section to specify the location of JavaScript files
WEB_DIRECTORY = "./js"