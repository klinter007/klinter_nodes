# Add Flexible Batch Image Node

## Why
Current image batching in ComfyUI can cause unwanted aspect ratio cropping when images of different dimensions are batched together. ComfyUI's tensor processing crops all images to match the first image's aspect ratio, which is often undesirable for workflows requiring preservation of original image dimensions. Users need a flexible batching solution that can handle 1-6 images and output them sequentially rather than as a cropped batch.

## What Changes
- Create a new `FlexibleBatchImage` node with 6 optional image inputs
- Implement sequential image output that preserves original aspect ratios
- Support dynamic batching from 1-6 images without aspect ratio constraints
- Create as standalone node initially (not registered in main node pack)
- Design for easy integration into klinter node pack after validation

## Impact
- Affected specs: New `image-processing` capability
- Affected code: New standalone node file `flexible_batch_image.py`
- User workflows: Enables aspect-ratio-preserving batch processing
- ComfyUI compatibility: Maintains standard node interface while working around tensor limitations

