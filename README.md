# Klinter Nodes for ComfyUI

## Overview
A collection of utility nodes for ComfyUI, including queue management and string manipulation tools.

## Key Features
- Queue management for efficient workflow execution
- String manipulation and concatenation tools
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

### Node Value to String
A node that converts node values into a formatted string, automatically using the connected nodes' names.
- **Inputs**: Variable number of inputs (1-1000) supporting STRING, INT, and FLOAT types
- **Features**:
  - Automatically uses connected nodes' names in the output
  - Formats float values to 4 decimal places
  - Outputs each value on a new line in "name:value" format
- **Example Output**:
  ```
  KSampler:20
  CLIPTextEncode:your prompt here
  VAEDecode:0.7500
  ```

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

## License
Open-source, free to use and modify

## Connect with Me
- Twitter: [@klinter_tech](https://twitter.com/klinter_tech)
- Instagram: [@klinter.ai](https://instagram.com/klinter.ai)
- GitHub: [klinter](https://github.com/klinter)
