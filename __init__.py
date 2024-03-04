# Import local node class modules
from .concat_klinter import concat_klinter
from .concat_klinter import whitelist
from .concat_klinter import PresentString
# Consider adding more imports here as necessary

# Mapping of node identifiers to their respective class implementations
NODE_CLASS_MAPPINGS = {
    "concat_klinter": concat_klinter,
    "whitelist": whitelist,
    "PresentString": PresentString,
    # You can add more node mappings here
}

# Mapping of node identifiers to their display names for UI or logging purposes
NODE_DISPLAY_NAME_MAPPINGS = {
    "concat_klinter": "Concat String (Klinter)",
    "whitelist": "Whitelist (Klinter)",
    "PresentString": "Show String (klinter)",
    # Additional display names can be added here
}

# Define what symbols this module exports
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
