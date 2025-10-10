"""Multi-image generation with aspect ratio templates using Google Gemini API."""

import os
import io
import torch
import numpy as np
from PIL import Image
from typing import Optional, Tuple, Any

# Try to import Google GenAI client for image generation
try:
    from google import genai
    from google.genai import types
    GOOGLE_GENAI_AVAILABLE = True
    USE_IMAGE_GENERATION = True
except ImportError:
    try:
        import google.generativeai as genai
        GOOGLE_GENAI_AVAILABLE = True
        USE_IMAGE_GENERATION = False
        print("Using text-only mode. For image generation, install: pip install google-genai")
    except ImportError:
        GOOGLE_GENAI_AVAILABLE = False
        USE_IMAGE_GENERATION = False
        print("No Google AI library found. Install with: pip install google-genai")

class NanoBananaMultiInput:
    """
    Nano Banana Multi Input - Multiple image editing and composition with aspect ratio control
    
    This node supports up to 5 input images and uses Google's Gemini API native aspect ratio
    configuration for precise image generation control. Calls Google's Gemini API directly 
    for creating and editing images using Google's state-of-the-art Gemini model.
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "prompt": ("STRING", {
                    "multiline": True, 
                    "default": "Create a beautiful landscape with mountains and a lake",
                    "placeholder": "Describe the image you want..."
                }),
            },
            "optional": {
                "image_1": ("IMAGE",),
                "image_2": ("IMAGE",),
                "image_3": ("IMAGE",),
                "image_4": ("IMAGE",),
                "image_5": ("IMAGE",),
                "aspect_ratio": (["passthrough", "1:1", "2:3", "3:2", "3:4", "4:3", "4:5", "5:4", "9:16", "16:9", "21:9"], {
                    "default": "passthrough"
                }),
                "api_key": ("STRING", {
                    "default": "",
                    "placeholder": "Optional: Override environment API key"
                }),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "STRING")
    RETURN_NAMES = ("generated_image", "description")
    FUNCTION = "process_images"
    CATEGORY = "klinter"
    NODE_COLOR = "#FFEB3B"  # Yellow for nano banana
    
    def __init__(self):
        # Get Gemini API key from environment variable (no hardcoding!)
        self.api_key = os.environ.get('GEMINI_API_KEY') or os.environ.get('GOOGLE_API_KEY')
        if not self.api_key:
            print("WARNING: GEMINI_API_KEY or GOOGLE_API_KEY environment variable not found.")
            print("Please set it in your environment or provide via node input!")
        
        # Initialize Gemini client if available
        self.model = None
        self.client = None
        self.init_client()
    
    def init_client(self, api_key=None):
        """Initialize the Gemini client with the provided or environment API key"""
        # Use provided API key or fall back to environment variable
        key_to_use = api_key if api_key else self.api_key
        
        if not key_to_use:
            print("No API key available for initialization")
            return False
        
        if GOOGLE_GENAI_AVAILABLE:
            try:
                if USE_IMAGE_GENERATION:
                    # Use Google GenAI for image generation
                    self.client = genai.Client(api_key=key_to_use)
                    print("Nano Banana Multi Input: Image generation client initialized successfully!")
                    return True
                else:
                    # Use Google Generative AI for text only
                    genai.configure(api_key=key_to_use)
                    self.model = genai.GenerativeModel('gemini-1.5-flash')
                    print("Nano Banana Multi Input: Text model initialized (text-only mode)!")
                    return True
            except Exception as e:
                print(f"Failed to initialize Nano Banana Multi Input client: {e}")
                return False
        return False
    
    def tensor_to_pil(self, tensor):
        """Convert ComfyUI tensor to PIL Image"""
        # ComfyUI tensors are in format [batch, height, width, channels] with values 0-1
        if tensor.dim() == 4:
            tensor = tensor.squeeze(0)  # Remove batch dimension
        
        # Convert from torch tensor to numpy
        if isinstance(tensor, torch.Tensor):
            tensor = tensor.cpu().numpy()
        
        # Ensure values are in 0-255 range
        if tensor.max() <= 1.0:
            tensor = tensor * 255
        
        # Ensure uint8 type
        tensor = tensor.astype(np.uint8)
        
        # Convert to PIL Image
        pil_image = Image.fromarray(tensor)
        return pil_image
    
    def pil_to_tensor(self, pil_image):
        """Convert PIL Image to ComfyUI tensor"""
        # Convert PIL to numpy array
        np_image = np.array(pil_image).astype(np.float32) / 255.0
        
        # Add batch dimension and convert to tensor
        tensor = torch.from_numpy(np_image).unsqueeze(0)
        return tensor
    
    
    def process_images(self, prompt: str, 
                      image_1: Optional[torch.Tensor] = None,
                      image_2: Optional[torch.Tensor] = None, 
                      image_3: Optional[torch.Tensor] = None,
                      image_4: Optional[torch.Tensor] = None,
                      image_5: Optional[torch.Tensor] = None,
                      aspect_ratio: str = "passthrough",
                      api_key: str = "") -> Tuple[torch.Tensor, str]:
        """
        Create or edit images using Google Gemini API with support for up to 5 input images
        and built-in aspect ratio configuration via the API
        """
        try:
            # Check if a custom API key was provided
            if api_key and api_key.strip():
                print("Using custom API key provided via node input")
                if not self.init_client(api_key.strip()):
                    raise ValueError("Failed to initialize client with provided API key")
            
            # Validate prerequisites
            if not GOOGLE_GENAI_AVAILABLE:
                raise ValueError("Google AI library not installed. Install with: pip install google-genai")
            
            if not (self.model or self.client):
                raise ValueError("Nano Banana Multi Input not initialized. Please provide API key via input or set GEMINI_API_KEY environment variable.")
            
            # Collect all provided images
            input_images = []
            pil_images = []
            
            for i, img in enumerate([image_1, image_2, image_3, image_4, image_5], 1):
                if img is not None:
                    pil_img = self.tensor_to_pil(img)
                    input_images.append(img)
                    pil_images.append(pil_img)
                    print(f"Input image {i} loaded: {pil_img.size}")
            
            # Prepare content for the API call
            contents = [prompt]
            
            # Determine mode automatically based on input images
            if len(pil_images) > 0:
                # Image editing/composition mode when images are provided
                print(f"Nano Banana Mode: Image Editing/Composition ({len(pil_images)} images)")
                print(f"Prompt: {prompt}")
                print(f"Aspect Ratio: {aspect_ratio}")
                
                # Add all input images
                contents.extend(pil_images)
            else:
                # Text-to-image mode when no images provided
                print("Nano Banana Mode: Text-to-Image Generation")
                print(f"Prompt: {prompt}")
                print(f"Aspect Ratio: {aspect_ratio}")
            
            print(f"Calling Google Gemini API with {len(contents)} content items...")
            
            if USE_IMAGE_GENERATION and self.client:
                # Use image generation capabilities
                print("Using image generation mode")
                
                # Generation configuration with aspect ratio
                generation_config = {
                    "temperature": 0.4,
                    "top_p": 0.8,
                    "max_output_tokens": 8192,
                }
                
                # Create the config object with aspect ratio if not passthrough
                if aspect_ratio != "passthrough":
                    config = types.GenerateContentConfig(
                        **generation_config,
                        image_config=types.ImageConfig(aspect_ratio=aspect_ratio)
                    )
                    print(f"Using aspect ratio configuration: {aspect_ratio}")
                else:
                    config = types.GenerateContentConfig(**generation_config)
                    print("Using passthrough mode - no aspect ratio override")
                
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash-image",
                    contents=contents,
                    config=config
                )
                
                # Process image generation response
                generated_images = []
                description_text = ""
                
                if response and response.candidates and len(response.candidates) > 0:
                    candidate = response.candidates[0]
                    
                    if hasattr(candidate.content, 'parts'):
                        for part in candidate.content.parts:
                            if hasattr(part, 'text') and part.text is not None:
                                description_text += part.text
                                print(f"Gemini response: {part.text[:100]}...")
                            elif hasattr(part, 'inline_data') and part.inline_data is not None:
                                # Convert inline image data to PIL Image
                                image_data = part.inline_data.data
                                pil_result = Image.open(io.BytesIO(image_data))
                                
                                # Convert to tensor
                                tensor = self.pil_to_tensor(pil_result)
                                generated_images.append(tensor)
                                print(f"Generated image size: {pil_result.size}")
                
                if generated_images:
                    # Return generated images
                    final_tensor = torch.cat(generated_images, dim=0)
                    print("Image generation completed successfully!")
                    return (final_tensor, f"{description_text}" if description_text else "Image created successfully!")
                else:
                    # Fallback if no images generated
                    if input_images:
                        fallback_image = input_images[0]
                    else:
                        # Default size 1024x1024 (matches API default)
                        fallback_image = torch.zeros(1, 1024, 1024, 3)
                    return (fallback_image, f"{description_text}" if description_text else "No image generated")
            
            else:
                # Use text-only mode as fallback
                print("Using text-only description mode")
                
                # Build description prompt
                if len(pil_images) > 0:
                    description_prompt = f"Analyze these {len(pil_images)} images and describe what this composition would look like: {prompt}"
                    
                    # Add prompt and all images
                    all_contents = [description_prompt]
                    all_contents.extend(pil_images)
                    
                    response = self.model.generate_content(all_contents)
                else:
                    # Text-only
                    response = self.model.generate_content(f"Describe in vivid detail an image with aspect ratio {aspect_ratio}: {prompt}")
                
                # Process text response
                description_text = response.text if hasattr(response, 'text') else str(response)
                print(f"Gemini response: {description_text[:200]}...")
                
                # Return original image(s) or placeholder with description
                if len(input_images) > 0:
                    print(f"Returning first of {len(input_images)} original images with description")
                    return (input_images[0], f"Description ({len(input_images)} images): {description_text}")
                else:
                    # Create placeholder with default size
                    placeholder = torch.full((1, 1024, 1024, 3), 0.9)
                    placeholder[:, :, :, 0] = 1.0  # Red channel
                    placeholder[:, :, :, 1] = 0.9  # Green channel  
                    placeholder[:, :, :, 2] = 0.3  # Blue channel
                    
                    print("Generated placeholder with description")
                    return (placeholder, f"Generated description: {description_text}")
        
        except Exception as e:
            error_msg = f"Nano Banana Multi Input Error: {str(e)}"
            print(error_msg)
            
            # Return fallback image
            try:
                if 'input_images' in locals() and len(input_images) > 0:
                    return (input_images[0], error_msg)
                elif image_1 is not None:
                    return (image_1, error_msg)
                else:
                    # Create error placeholder
                    error_image = torch.zeros(1, 1024, 1024, 3)
                    error_image[:, :, :, 0] = 0.8  # Reddish error color
                    return (error_image, error_msg)
            except:
                # Ultimate fallback
                black_image = torch.zeros(1, 1024, 1024, 3)
                return (black_image, error_msg)

# Register the node
NODE_CLASS_MAPPINGS = {
    "NanoBananaMultiInput": NanoBananaMultiInput
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "NanoBananaMultiInput": "Nano Banana Multi Input - Klinter"
}

# Export the class
__all__ = ['NanoBananaMultiInput']
