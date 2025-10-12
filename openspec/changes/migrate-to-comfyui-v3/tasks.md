# Implementation Tasks

## 1. Update Simple String Nodes
- [ ] 1.1 Migrate `concat_string.py` to V3 schema
- [ ] 1.2 Migrate `filter_string.py` to V3 schema
- [ ] 1.3 Migrate `string_contact_multi.py` to V3 schema
- [ ] 1.4 Migrate `node_value_to_string.py` to V3 schema

## 2. Update Image Processing Nodes
- [ ] 2.1 Migrate `load_image_plus.py` to V3 schema
- [ ] 2.2 Migrate `aspect_selector.py` to V3 schema
- [ ] 2.3 Migrate `size_selector.py` to V3 schema
- [ ] 2.4 Migrate `bbox_cropper.py` to V3 schema
- [ ] 2.5 Migrate `outpaint_padding.py` to V3 schema
- [ ] 2.6 Migrate `zoom_out_composer.py` to V3 schema
- [ ] 2.7 Migrate `folder_loader.py` to V3 schema
- [ ] 2.8 Migrate `flexible_batch_image.py` to V3 schema

## 3. Update Video Processing Nodes
- [ ] 3.1 Migrate `video_extend.py` (both LoadVideoForExtending and PrepVideoForExtend) to V3 schema
- [ ] 3.2 Migrate `video_from_folder.py` to V3 schema
- [ ] 3.3 Migrate `speed_ramp.py` to V3 schema

## 4. Update Utility and Special Nodes
- [ ] 4.1 Migrate `yellow_bus.py` (with AnyType wildcard handling) to V3 schema
- [ ] 4.2 Migrate `output_tester.py` to V3 schema
- [ ] 4.3 Migrate `json_extractor.py` to V3 schema
- [ ] 4.4 Migrate `save_audio_plus.py` (extends ComfyUI's SaveAudio) to V3 schema
- [ ] 4.5 Migrate `nano_banana_multi_input.py` to V3 schema

## 5. Update Node Registration System
- [ ] 5.1 Update `__init__.py` to use ComfyExtension class
- [ ] 5.2 Create `comfy_entrypoint()` function
- [ ] 5.3 Remove legacy NODE_CLASS_MAPPINGS and NODE_DISPLAY_NAME_MAPPINGS dictionaries
- [ ] 5.4 Ensure WEB_DIRECTORY and WEB_EXTENSIONS remain functional

## 6. Update Project Documentation
- [ ] 6.1 Update `openspec/project.md` with V3 schema conventions
- [ ] 6.2 Update README.md with V3 migration notes and ComfyUI version requirements
- [ ] 6.3 Add migration guide for any external users of these nodes

## 7. Testing and Validation
- [ ] 7.1 Test all string manipulation nodes in ComfyUI
- [ ] 7.2 Test all image processing nodes in ComfyUI
- [ ] 7.3 Test all video processing nodes in ComfyUI
- [ ] 7.4 Test special nodes (YellowBus, OutputTester, etc.) in ComfyUI
- [ ] 7.5 Verify example workflows still function correctly
- [ ] 7.6 Test that JavaScript UI extensions still work properly

