# ComfyUI Nodes Specification

## ADDED Requirements

### Requirement: V3 Schema Node Definition
All nodes SHALL be defined using ComfyUI V3 schema by inheriting from `io.ComfyNode` and implementing the `define_schema()` classmethod that returns an `io.Schema` object containing node metadata, inputs, and outputs.

#### Scenario: Simple string concatenation node
- **WHEN** defining a node that concatenates strings
- **THEN** the node SHALL inherit from `io.ComfyNode`
- **AND** implement `define_schema()` returning `io.Schema` with `node_id`, `display_name`, `category`, `inputs`, and `outputs`
- **AND** define inputs using `io.String.Input()` objects
- **AND** define outputs using `io.String.Output()` objects

#### Scenario: Image processing node with optional inputs
- **WHEN** defining a node that processes images with optional parameters
- **THEN** inputs SHALL be defined using type-specific classes like `io.Image.Input()`, `io.Int.Input()`, `io.Float.Input()`
- **AND** optional inputs SHALL use `optional=True` parameter
- **AND** input parameters like `default`, `min`, `max`, `step` SHALL be passed as arguments to Input constructors

#### Scenario: Dynamic type node (AnyType wildcard)
- **WHEN** defining a node that accepts any input type (like YellowBus)
- **THEN** use `io.Custom("*").Input()` for wildcard type handling
- **AND** outputs SHALL use `io.Custom("*").Output()` for dynamic output types

### Requirement: Standardized Execute Method
All nodes SHALL implement their execution logic in a classmethod named `execute` that returns an `io.NodeOutput` object.

#### Scenario: Node with single output
- **WHEN** a node execution completes successfully
- **THEN** return `io.NodeOutput(result)` with the result value
- **AND** the result type SHALL match the declared output type in schema

#### Scenario: Node with multiple outputs
- **WHEN** a node returns multiple values
- **THEN** return `io.NodeOutput(value1, value2, value3)` with all output values in order
- **AND** the number of values SHALL match the number of outputs in schema

#### Scenario: Node with UI preview
- **WHEN** a node should display preview in UI (like images)
- **THEN** return `io.NodeOutput(result, ui=ui.PreviewImage(result, cls=cls))`
- **AND** import UI helpers from `comfy_api.latest.ui`

### Requirement: Input Validation
Nodes that require input validation SHALL implement the `validate_inputs()` classmethod (renamed from V1's `VALIDATE_INPUTS`).

#### Scenario: Successful validation
- **WHEN** all inputs are valid
- **THEN** `validate_inputs()` SHALL return `True`

#### Scenario: Failed validation
- **WHEN** an input is invalid
- **THEN** `validate_inputs()` SHALL return an error string describing the issue
- **AND** the node execution SHALL not proceed

### Requirement: Cache Control via Fingerprinting
Nodes that need to control cache behavior SHALL implement the `fingerprint_inputs()` classmethod (renamed from V1's `IS_CHANGED` for clarity).

#### Scenario: File-based input fingerprinting
- **WHEN** a node loads external files (like LoadImagePlus)
- **THEN** `fingerprint_inputs()` SHALL return a hash of the file content
- **AND** node SHALL re-execute when the hash changes
- **AND** node SHALL use cached result when hash remains the same

#### Scenario: Time-based fingerprinting
- **WHEN** a node should re-execute every time
- **THEN** `fingerprint_inputs()` SHALL return a unique value (like timestamp)

### Requirement: Extension Registration System
All nodes SHALL be registered through a `ComfyExtension` class and exposed via the `comfy_entrypoint()` function instead of dictionary-based registration.

#### Scenario: Single extension with multiple nodes
- **WHEN** packaging multiple nodes in one extension
- **THEN** create a class inheriting from `ComfyExtension`
- **AND** implement async `get_node_list()` method returning list of node classes
- **AND** define async `comfy_entrypoint()` function returning the extension instance

#### Scenario: Maintaining JavaScript extensions
- **WHEN** the extension includes JavaScript UI enhancements
- **THEN** the extension class MAY define `WEB_DIRECTORY` attribute
- **AND** MAY define `WEB_EXTENSIONS` list of JavaScript files

### Requirement: Stateless Node Architecture
Node classes SHALL be stateless with all methods defined as classmethods, and SHALL NOT use `__init__` methods for instance state.

#### Scenario: Node without instance state
- **WHEN** defining any node in V3 schema
- **THEN** all methods SHALL be classmethods (using `@classmethod` decorator)
- **AND** no `__init__` method SHALL be defined
- **AND** no instance variables SHALL be used

#### Scenario: Node requiring shared state
- **WHEN** a node requires persistent state across executions
- **THEN** use module-level variables or external state management
- **AND** NOT instance variables (which have no effect in V3)

### Requirement: Custom Type Support
Nodes SHALL support custom input/output types using either `io.Custom()` helper or custom type class definitions.

#### Scenario: Using Custom helper for simple types
- **WHEN** defining a node with a custom type
- **THEN** use `io.Custom("MY_CUSTOM_TYPE").Input("name")` for inputs
- **AND** use `io.Custom("MY_CUSTOM_TYPE").Output()` for outputs

#### Scenario: Defining reusable custom type class
- **WHEN** a custom type is used across multiple nodes
- **THEN** define a class decorated with `@io.comfytype(io_type="MY_TYPE")`
- **AND** implement `Type` attribute for Python type hint
- **AND** implement nested `Input` and `Output` classes inheriting from `io.Input` and `io.Output`

### Requirement: Output Node Designation
Nodes that produce side effects (like saving files) SHALL be marked as output nodes in their schema.

#### Scenario: File-saving node
- **WHEN** a node saves files or produces side effects
- **THEN** set `is_output_node=True` in the Schema definition
- **AND** the ComfyUI UI SHALL display a "run" button for partial graph execution

### Requirement: API Version Management
All nodes SHALL import from a specific ComfyUI API version to ensure stability.

#### Scenario: Using stable API version
- **WHEN** implementing production nodes
- **THEN** import from `comfy_api.v0_0_2` (or latest stable version)

#### Scenario: Using latest development API
- **WHEN** developing new features requiring cutting-edge APIs
- **THEN** import from `comfy_api.latest`
- **AND** be aware that breaking changes may occur in latest

