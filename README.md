# Klinter Nodes for ComfyUI

A collection of utility nodes for ComfyUI that enhance workflow creation and management. These nodes are designed to make common tasks easier and more efficient.

## About the Author

You can find me on:
- X (Twitter): [@giliBenShahar](https://x.com/giliBenShahar)
- Instagram: [@gilibenshahar](https://instagram.com/gilibenshahar)
- CivitAI: [klinter](https://civitai.com/user/klinter) - Check out my Loras, models, and occasional workflows!
- Discord: Find me on the [Banadoco Discord Server](https://discord.gg/Hvdfr7ht), a great community for AI creators and researchers.

## Table of Contents
- [Aspect Ratio Selector](#aspect-ratio-selector)
- [String Concatenation](#string-concatenation)
- [Filter String](#filter-string)
- [Size Selector](#size-selector)
- [Folder Loader](#folder-loader)
- [Load Image Plus](#load-image-plus)
- [Extra Padding](#extra-padding)
- [Zoom Out Composer](#zoom-out-composer)
- [Speed Ramp](#speed-ramp)

## Available Nodes

### Aspect Ratio Selector
A flexible node for managing image dimensions with common aspect ratios.

**Features:**
- Base resolution selection (512, 768, 1024, 1536)
- Common aspect ratios (1:1, 3:4, 5:8, 9:16, 9:21, 4:3, 3:2, 16:9, 21:9)
- Random aspect ratio selection using ComfyUI's seed system
- Maintains proper proportions across all base resolutions

**Inputs:**
- Base Resolution: Select the base size for calculations
- Aspect Ratio: Choose from common ratios
- Seed: Control random selection (uses ComfyUI's seed modes)

**Outputs:**
- Width: Calculated width
- Height: Calculated height
- Name: Selected aspect ratio

### String Concatenation
Combines multiple text strings, useful for building prompts.

**Features:**
- Combines two strings with optional separator
- Useful for dynamic prompt building

**Inputs:**
- String 1: First text string
- String 2: Second text string
- Separator: Text to insert between strings (optional)

**Outputs:**
- String: Combined text result

### Filter String
Filters and replaces specified words in text strings.

**Features:**
- Word replacement system
- Customizable filter list
- Maintains text structure

### Size Selector
Loads predefined image sizes from an external list.

**Features:**
- External size definitions
- Quick size selection
- Commonly used dimensions

### Folder Loader
Enables loading images from a specified path - particularly useful when working with the Zoom Out Composer for loading sequential images.

### Load Image Plus
Standard image loading functionality with an additional filename output - useful when you need to track or use the original filename in your workflow.

### Extra Padding
Adds padding to images with various options.

### Zoom Out Composer
Creates seamless infinite zoom animations by intelligently stitching images together. Perfect for creating mesmerizing zoom-out effects with your image sequence.

### Speed Ramp
A sophisticated video speed manipulation node that creates dynamic speed effects.

**Features:**
- Built-in speed curve presets:
  * Double Peak: Creates two speed-up moments
  * Quad Burst: Creates an intense speed-up with four peaks
- Custom speed value support
- Frame interpolation for smooth transitions
- Base FPS control (1-120 fps)

**Inputs:**
- Frames: Input image sequence
- Use Preset: Toggle between preset curves and custom speed
- Preset Curve: Choose from "double_peak" or "quad_burst" presets
- Base FPS: Set the base frame rate (1-120)
- Speed Values: Custom speed multiplier (0.1x to 10x)

**Outputs:**
- Frames: Speed-adjusted image sequence

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the terms specified in the LICENSE file.
