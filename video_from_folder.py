"""Node for loading a single video from a folder using seed-based selection."""

import os
import torch
import numpy as np
import random
import folder_paths
from comfy_api.latest import io

# Try to import video reading libraries
try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False

try:
    import imageio
    HAS_IMAGEIO = True
except ImportError:
    HAS_IMAGEIO = False

try:
    import subprocess
    import json
    HAS_FFMPEG = True
except ImportError:
    HAS_FFMPEG = False

class VideoFromFolder(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        """Define the schema for the video from folder node.
        
        Returns:
            io.Schema: Node schema with inputs and outputs
        """
        return io.Schema(
            node_id="VideoFromFolder",
            display_name="Video From Folder - Klinter",
            category="klinter",
            description="Load a single video from a folder using seed-based selection",
            inputs=[
                io.String.Input("folder_path", default=""),
                io.Int.Input("seed", default=0, min=0, max=0xffffffffffffffff),
                io.Combo.Input("seed_mode", options=["increment", "random", "fixed"]),
                io.Int.Input("seed_offset", default=0, min=0, step=1, optional=True),
            ],
            outputs=[
                io.Image.Output(display_name="frames"),
                io.String.Output(display_name="video_path"),
                io.Int.Output(display_name="video_index"),
                io.Float.Output(display_name="fps"),
                io.Float.Output(display_name="duration"),
                io.Int.Output(display_name="frame_count")
            ]
        )

    @classmethod
    def fingerprint_inputs(cls, folder_path, seed, seed_mode, seed_offset=0):
        """Tell ComfyUI when the node output changes (renamed from IS_CHANGED)."""
        # For increment mode, always mark as changed so it increments each run
        if seed_mode == "increment":
            return float("NaN")
        # For random mode with same seed, return same video
        return f"{folder_path}_{seed}_{seed_mode}_{seed_offset}"

    @classmethod
    def get_video_files(cls, folder_path):
        """Get sorted list of video files in the folder."""
        if not os.path.isdir(folder_path):
            raise FileNotFoundError(f"Folder '{folder_path}' cannot be found.")
        
        valid_extensions = {'.mp4', '.mov', '.avi', '.mkv', '.webm', '.m4v'}
        video_files = sorted([
            f for f in os.listdir(folder_path)
            if os.path.splitext(f.lower())[1] in valid_extensions
        ])
        
        if not video_files:
            raise ValueError(f"No video files found in folder: {folder_path}")
        
        return video_files

    @classmethod
    def get_video_info(cls, video_path):
        """Get video information using available methods."""
        # Try cv2 first
        if HAS_CV2:
            try:
                cap = cv2.VideoCapture(video_path)
                if cap.isOpened():
                    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
                    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                    duration = frame_count / fps if fps > 0 else 0
                    cap.release()
                    
                    return {
                        'fps': fps,
                        'width': width,
                        'height': height,
                        'duration': duration,
                        'frame_count': frame_count
                    }
            except Exception as e:
                print(f"cv2 failed to get video info: {e}")
        
        # Try imageio
        if HAS_IMAGEIO:
            try:
                reader = imageio.get_reader(video_path)
                meta = reader.get_meta_data()
                fps = meta.get('fps', 24.0)
                width = meta.get('size', [1920, 1080])[0]
                height = meta.get('size', [1920, 1080])[1]
                duration = meta.get('duration', 0)
                reader.close()
                
                return {
                    'fps': fps,
                    'width': width,
                    'height': height,
                    'duration': duration
                }
            except Exception as e:
                print(f"imageio failed to get video info: {e}")
        
        # Try ffprobe if available
        if HAS_FFMPEG:
            try:
                cmd = [
                    'ffprobe',
                    '-v', 'quiet',
                    '-print_format', 'json',
                    '-show_format',
                    '-show_streams',
                    video_path
                ]
                result = subprocess.run(cmd, capture_output=True, text=True, check=True)
                data = json.loads(result.stdout)
                
                video_stream = None
                for stream in data.get('streams', []):
                    if stream.get('codec_type') == 'video':
                        video_stream = stream
                        break
                
                if video_stream:
                    fps_str = video_stream.get('r_frame_rate', '24/1')
                    if '/' in fps_str:
                        num, den = map(int, fps_str.split('/'))
                        fps = num / den if den != 0 else 24.0
                    else:
                        fps = float(fps_str)
                    
                    return {
                        'fps': fps,
                        'width': int(video_stream.get('width', 1920)),
                        'height': int(video_stream.get('height', 1080)),
                        'duration': float(data.get('format', {}).get('duration', 0))
                    }
            except Exception as e:
                print(f"ffprobe failed: {e}")
        
        # Return defaults if all methods fail
        print(f"Warning: Could not get video info for {video_path}, using defaults")
        return {
            'fps': 24.0,
            'width': 1920,
            'height': 1080,
            'duration': 0
        }

    @classmethod
    def load_video_frames(cls, video_path):
        """Load video and convert to tensor of frames using available methods.
        
        Returns:
            Tuple of (frames tensor, fps, duration, frame_count)
        """
        frames = []
        info = cls.get_video_info(video_path)
        
        # Try cv2 first (most reliable and commonly available)
        if HAS_CV2:
            try:
                cap = cv2.VideoCapture(video_path)
                if cap.isOpened():
                    while True:
                        ret, frame = cap.read()
                        if not ret:
                            break
                        # Convert BGR to RGB
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        frame_tensor = torch.from_numpy(frame_rgb.astype(np.float32) / 255.0)
                        frames.append(frame_tensor)
                    cap.release()
                    
                    if frames:
                        frame_count = len(frames)
                        duration = frame_count / info['fps'] if info['fps'] > 0 else 0
                        return torch.stack(frames), info['fps'], duration, frame_count
                    else:
                        print("cv2: No frames extracted")
            except Exception as e:
                print(f"cv2 failed to load video: {e}")
                frames = []  # Reset frames if cv2 failed
        
        # Try imageio if cv2 failed or not available
        if HAS_IMAGEIO and not frames:
            try:
                reader = imageio.get_reader(video_path)
                for frame in reader:
                    frame_tensor = torch.from_numpy(frame.astype(np.float32) / 255.0)
                    frames.append(frame_tensor)
                reader.close()
                
                if frames:
                    frame_count = len(frames)
                    duration = frame_count / info['fps'] if info['fps'] > 0 else 0
                    return torch.stack(frames), info['fps'], duration, frame_count
                else:
                    print("imageio: No frames extracted")
            except Exception as e:
                print(f"imageio failed to load video: {e}")
                frames = []  # Reset frames if imageio failed
        
        # Try ffmpeg as last resort
        if HAS_FFMPEG and not frames:
            try:
                # Check if ffmpeg is actually available in system
                subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
                
                cmd = [
                    'ffmpeg',
                    '-i', video_path,
                    '-f', 'image2pipe',
                    '-pix_fmt', 'rgb24',
                    '-vcodec', 'rawvideo',
                    '-'
                ]
                
                process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
                
                frame_size = info['width'] * info['height'] * 3
                
                while True:
                    raw_frame = process.stdout.read(frame_size)
                    if len(raw_frame) != frame_size:
                        break
                    
                    frame = np.frombuffer(raw_frame, dtype=np.uint8)
                    frame = frame.reshape((info['height'], info['width'], 3))
                    frame_tensor = torch.from_numpy(frame.astype(np.float32) / 255.0)
                    frames.append(frame_tensor)
                
                process.stdout.close()
                process.wait()
                
                if frames:
                    frame_count = len(frames)
                    duration = frame_count / info['fps'] if info['fps'] > 0 else 0
                    return torch.stack(frames), info['fps'], duration, frame_count
            except FileNotFoundError:
                print("ffmpeg not found in system PATH")
            except Exception as e:
                print(f"ffmpeg failed to load video: {e}")
        
        # If all methods failed
        if not frames:
            error_msg = "Could not load video. Please install one of: "
            requirements = []
            if not HAS_CV2:
                requirements.append("opencv-python (pip install opencv-python)")
            if not HAS_IMAGEIO:
                requirements.append("imageio[ffmpeg] (pip install imageio[ffmpeg])")
            if not HAS_FFMPEG:
                requirements.append("ffmpeg (system package)")
            
            raise ValueError(error_msg + ", ".join(requirements))
        
        frame_count = len(frames)
        duration = frame_count / info['fps'] if info['fps'] > 0 else 0
        return torch.stack(frames), info['fps'], duration, frame_count

    @classmethod
    def calculate_video_index(cls, seed, seed_mode, seed_offset, num_videos):
        """Calculate which video index to use based on seed and mode."""
        if seed_mode == "random":
            # Use seed for reproducible randomness
            rng = random.Random(seed + seed_offset)
            return rng.randint(0, num_videos - 1)
        elif seed_mode == "increment":
            # Increment mode: seed acts as counter, offset adds to it
            index = seed + seed_offset
        else:  # fixed
            # Fixed mode: always use seed_offset as the index
            index = seed_offset
        
        # Handle looping when index exceeds number of videos
        return index % num_videos

    @classmethod
    def execute(cls, folder_path, seed, seed_mode, seed_offset=0) -> io.NodeOutput:
        """Load a single video from folder based on seed selection.
        
        Args:
            folder_path: Path to folder containing video files
            seed: Seed value for selection
            seed_mode: 'increment', 'random', or 'fixed'
            seed_offset: Additional offset to apply to the selection
        
        Returns:
            io.NodeOutput: Frames tensor, video path, video index, fps, duration, frame_count
        """
        # Get all video files in the folder
        video_files = cls.get_video_files(folder_path)
        num_videos = len(video_files)
        
        # Calculate which video to load
        video_index = cls.calculate_video_index(seed, seed_mode, seed_offset, num_videos)
        
        # Get the selected video file
        selected_video = video_files[video_index]
        full_video_path = os.path.join(folder_path, selected_video)
        
        print(f"Loading video {video_index + 1}/{num_videos}: {selected_video}")
        print(f"Seed: {seed}, Mode: {seed_mode}, Offset: {seed_offset}")
        
        # Load the video frames
        frames, fps, duration, frame_count = cls.load_video_frames(full_video_path)
        
        return io.NodeOutput(frames, full_video_path, video_index, fps, duration, frame_count)

# Register the node
NODE_CLASS_MAPPINGS = {
    "VideoFromFolder": VideoFromFolder
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "VideoFromFolder": "Video From Folder - Klinter"
}

# Export the class
__all__ = ['VideoFromFolder']
