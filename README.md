# Klinter Nodes for ComfyUI

## Overview
A collection of utility nodes for ComfyUI, including queue management, string manipulation, and node value conversion tools.

## Key Features
- Queue management for efficient workflow execution
- String manipulation and concatenation tools
- Node value to string conversion
- Dynamic input handling
- Memory-efficient processing

## Nodes

### Queue Counter
A floating widget that lets you:
- Set number of runs (1-255)
- Start/Stop batch processing
- Monitor current run progress
- Track total runs completed

### String Contact Multi
A dynamic string concatenation node that allows:
- Variable number of string inputs (2-1000)
- Multiple separator options (comma, newline, pipe, space)
- Easy input management with "Update inputs" button
- Perfect for combining prompts or text elements

### Node Value to String Multi
A versatile node for converting multiple node values to formatted strings:
- Dynamic input count (2-1000 inputs)
- Automatically detects and displays connected node names
- Supports various input types (STRING, INT, FLOAT)
- Formats values with their source node names
- Useful for logging, debugging, and workflow tracking

### Node Value to String
A simple, single-input version of the node value to string conversion:
- Takes one input of any type
- Converts input to a formatted string
- Displays the source node's name
- Ideal for quick value inspection or simple logging

## Installation
1. Place in ComfyUI's `custom_nodes` directory
2. Restart ComfyUI

## Configuration
- Enable/Disable queue widget in ComfyUI Settings
- Adjust run count directly in the widget
- Widget can be dragged anywhere on the interface

## Benefits
- Prevent system slowdowns
- Controlled batch processing
- Easy workflow iteration
- Flexible string manipulation
- Advanced node value tracking

## License
Open-source, free to use and modify

## Connect with Me
- Twitter: [@klinter_tech](https://twitter.com/klinter_tech)
- Instagram: [@klinter.ai](https://instagram.com/klinter.ai)
- GitHub: [klinter](https://github.com/klinter)
