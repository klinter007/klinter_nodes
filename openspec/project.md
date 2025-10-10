# Project Context

## Purpose
Klinter Nodes is a collection of custom nodes designed to enhance ComfyUI workflows for AI art generation. The project provides flexible and powerful tools for image processing, string manipulation, video processing, and workflow utilities that extend ComfyUI's native capabilities. Each node is designed to solve specific workflow pain points while maintaining ComfyUI's node-based paradigm.

## Tech Stack
- **Python 3.x** - Backend node implementations, core logic
- **JavaScript/ES6** - Frontend UI extensions, dynamic node behavior
- **ComfyUI Framework** - Node registration, execution engine, UI integration
- **JSON** - Configuration files, workflow definitions, node metadata
- **Pillow/PIL** - Image processing operations
- **NumPy** - Array operations and mathematical computations

## Project Conventions

### Code Style
- **Python**: Follow PEP 8 standards with descriptive docstrings for all classes and methods
- **Naming Conventions**:
  - Classes: PascalCase (e.g., `YellowBus`, `OutpaintPadding`)
  - Functions/Methods: snake_case (e.g., `route`, `INPUT_TYPES`)
  - Node IDs: kebab-case for internal mapping (e.g., `"concat"`, `"filter"`)
  - Display Names: Human-readable with "klinter" suffix (e.g., `"Yellow Bus - klinter"`)
- **JavaScript**: ES6+ with consistent indentation, meaningful variable names
- **Type Handling**: Use `AnyType` wildcard pattern for dynamic type adaptation
- **Documentation**: Include purpose and usage description in node class docstrings

### Architecture Patterns
- **Node-based Plugin Architecture**: Each node is self-contained with clear input/output definitions
- **Dynamic Type System**: Nodes adapt types based on connections (using `AnyType` pattern)
- **Separation of Concerns**: Python handles logic, JavaScript handles UI behavior
- **Registry Pattern**: Central node mappings in `__init__.py` for registration
- **Configuration-driven**: External JSON files for complex data (e.g., `sizes.json`)
- **Modular Design**: Each node in its own file with consistent structure
- **UI Extension Pattern**: JavaScript extensions for dynamic node behavior

### Testing Strategy
- Focus on workflow integration testing via example JSON workflows
- Manual testing through ComfyUI interface
- Validation through `VALIDATE_INPUTS` classmethod where needed

### Git Workflow
- Main branch for stable releases
- Feature branches for new node development
- Clean commit messages describing node functionality
- Keep untracked files (`.DS_Store`, `.cursor/`) out of repository

## Domain Context
**ComfyUI Ecosystem**: ComfyUI is a node-based interface for AI art generation where users create workflows by connecting nodes. Each node performs specific operations (prompting, image generation, processing, etc.).

**Key ComfyUI Concepts**:
- **Nodes**: Processing units with inputs, outputs, and parameters
- **Node Registration**: Nodes must be registered with `NODE_CLASS_MAPPINGS` and `NODE_DISPLAY_NAME_MAPPINGS`
- **Dynamic Types**: Nodes can accept multiple types using wildcard patterns
- **UI Extensions**: JavaScript files can enhance node behavior in the frontend
- **Workflows**: JSON-serialized node graphs that define processing pipelines

**Klinter Node Categories**:
- **String Manipulation**: Concat, filter, multi-contact operations
- **Image Processing**: Loading, cropping, aspect handling, outpainting
- **Video Processing**: Loading, extending, folder-based video creation
- **Workflow Utilities**: Dynamic routing (Yellow Bus), debugging, output testing

## Important Constraints
- **ComfyUI Compatibility**: All nodes must follow ComfyUI's node interface requirements
- **Python/JavaScript Bridge**: Backend Python logic with optional frontend JavaScript enhancements
- **Type System**: Support ComfyUI's dynamic typing with `AnyType` for flexible connections
- **UI Consistency**: All nodes use "klinter" branding in display names
- **Resource Management**: Handle file I/O operations safely for batch processing
- **No Hard-coded Prompts**: Prompt rulesets managed from config files and settings [[memory:4093722]]

## External Dependencies
- **ComfyUI Core**: Node registration system, execution engine, UI framework
- **Python Standard Library**: File I/O, JSON processing, string operations
- **Pillow (PIL)**: Image processing and manipulation
- **NumPy**: Array operations for numerical computations
- **Node.js/Browser APIs**: For JavaScript UI extensions
- **LiteGraph**: ComfyUI's underlying graph visualization library
