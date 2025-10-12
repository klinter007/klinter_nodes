# Migration to ComfyUI V3 Node Schema

## Why
ComfyUI has introduced a new V3 schema that provides a more organized and maintainable way of defining custom nodes. The V3 schema uses a versioned API (`comfy_api.v0_0_2` and `comfy_api.latest`) and future node features will only be available in V3. Migrating now ensures our nodes remain compatible with future ComfyUI versions and allows us to benefit from improved type safety, better code organization, and enhanced UI capabilities.

## What Changes
- **BREAKING**: All node classes will inherit from `io.ComfyNode` instead of plain classes
- **BREAKING**: `INPUT_TYPES()` classmethod replaced with `define_schema()` returning `io.Schema` objects
- **BREAKING**: `RETURN_TYPES`, `RETURN_NAMES`, `FUNCTION`, `CATEGORY` class properties moved into `io.Schema`
- **BREAKING**: All execution methods renamed from various names to standardized `execute()` classmethod
- **BREAKING**: `VALIDATE_INPUTS` renamed to `validate_inputs` (lowercase)
- **BREAKING**: `IS_CHANGED` renamed to `fingerprint_inputs` for clarity
- **BREAKING**: Node registration in `__init__.py` changes from `NODE_CLASS_MAPPINGS` dictionaries to `ComfyExtension` class with `comfy_entrypoint()` function
- Update all return statements to use `io.NodeOutput` wrapper
- Import from `comfy_api.latest` (or specific version like `v0_0_2`) instead of direct ComfyUI imports
- Remove `__init__` methods from node classes (V3 nodes are stateless with classmethods only)
- Update `OUTPUT_NODE` property to `is_output_node` in Schema
- Update input/output definitions to use type objects (`io.Image.Input()`, `io.String.Input()`, etc.) instead of string tuples

## Impact
- **Affected specs**: All ComfyUI node capabilities (creating new capability)
- **Affected code**: ALL node files (20 Python files):
  - `aspect_selector.py`
  - `bbox_cropper.py`
  - `concat_string.py`
  - `filter_string.py`
  - `flexible_batch_image.py`
  - `folder_loader.py`
  - `json_extractor.py`
  - `load_image_plus.py`
  - `nano_banana_multi_input.py`
  - `node_value_to_string.py`
  - `outpaint_padding.py`
  - `output_tester.py`
  - `save_audio_plus.py`
  - `size_selector.py`
  - `speed_ramp.py`
  - `string_contact_multi.py`
  - `video_extend.py` (2 nodes)
  - `video_from_folder.py`
  - `yellow_bus.py`
  - `zoom_out_composer.py`
  - `__init__.py` (node registration)
- **Breaking change**: Users must have ComfyUI version that supports V3 schema (comfy_api package)
- **No workflow changes**: End-user workflows remain compatible (node IDs and behavior unchanged)
- **JavaScript files**: No changes needed (UI extensions remain compatible)

