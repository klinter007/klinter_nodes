# Import local node class modules
from .nodes import concat
from .nodes import Filter
from .nodes import PresentString
from .nodes import SizeSelector
from .nodes import SingleString
from .nodes import YellowBus
from .nodes import Florence2Captions2IPA

# Consider adding more imports here as necessary

# Mapping of node identifiers to their respective class implementations
NODE_CLASS_MAPPINGS = {
    "concat": concat,
    "Filter": Filter,
    "PresentString": PresentString,
    "SizeSelector": SizeSelector,
    "SingleString": SingleString,
    "YellowBus": YellowBus,
    "Florence2Captions2IPA":Florence2Captions2IPA,

    # You can add more node mappings here
}

# Mapping of node identifiers to their display names for UI or logging purposes
NODE_DISPLAY_NAME_MAPPINGS = {
    "concat": "Concat String (Klinter)",
    "Filter": "Filter (Klinter)",
    "PresentString": "Show String (klinter)",
    "SizeSelector": "Size Selector (klinter)",
    "SingleString": "Single String (klinter)",
    "YellowBus": "YellowBus (klinter)",
    "Florence2Captions2IPA":"Florence2Captions2IPA (klinter)",
    # Additional display names can be added here
}

# Define what symbols this module exports
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS']
