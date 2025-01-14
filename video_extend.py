"""Nodes for loading and preparing videos for extension."""

import os
import subprocess
import torch
from shutil import copyfile
import folder_paths
from comfy.utils import ProgressBar

UPLOAD_FOLDER = folder_paths.get_input_directory()

class LoadVideoForExtending:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "video": ("VIDEO",),  # Special upload type that will be handled by the frontend
            }
        }

    RETURN_TYPES = ("IMAGE", "TUPLE")  # frames tensor and video info tuple
    RETURN_NAMES = ("frames", "video_info")
    FUNCTION = "load_video"
    CATEGORY = "Klinter"

    def _get_video_info(self, video_path: str) -> dict:
        """Get video information using ffprobe.
        
        Args:
            video_path: Path to the video file
            
        Returns:
            Dictionary containing video metadata (fps, width, height, duration)
        """
        # First, get frame rate
        fps_cmd = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=r_frame_rate',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]
        
        fps_result = subprocess.run(fps_cmd, capture_output=True, text=True)
        if fps_result.returncode != 0:
            raise RuntimeError(f"FFprobe error (fps): {fps_result.stderr}")
            
        fps_str = fps_result.stdout.strip()
        if '/' in fps_str:
            fps_num, fps_den = map(int, fps_str.split('/'))
            fps = fps_num / fps_den
        else:
            fps = float(fps_str)

        # Then get other stream information
        info_cmd = [
            'ffprobe',
            '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]
        
        info_result = subprocess.run(info_cmd, capture_output=True, text=True)
        if info_result.returncode != 0:
            raise RuntimeError(f"FFprobe error (info): {info_result.stderr}")
            
        width, height = map(int, info_result.stdout.strip().split('\n'))
        
        # Finally get duration
        duration_cmd = [
            'ffprobe',
            '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            video_path
        ]
        
        duration_result = subprocess.run(duration_cmd, capture_output=True, text=True)
        if duration_result.returncode != 0:
            raise RuntimeError(f"FFprobe error (duration): {duration_result.stderr}")
            
        duration = float(duration_result.stdout.strip())

        return {
            'fps': fps,
            'width': width,
            'height': height,
            'duration': duration
        }

    @classmethod
    def IS_CHANGED(cls, video):
        """Tell ComfyUI that the output depends on the video file."""
        image_path = folder_paths.get_annotated_filepath(video)
        if image_path is None:
            return False
        return os.path.getmtime(image_path)

    @classmethod
    def VALIDATE_INPUTS(cls, video):
        """Validate that the video file exists."""
        if not folder_paths.exists_annotated_filepath(video):
            return "Video file not found: {}".format(video)
        return True

    def load_video(self, video: str):
        """Load video and convert to tensor of frames.
        
        Args:
            video: Name or path of the video file
            
        Returns:
            Tuple of (frames tensor, video info tuple)
        """
        video_path = folder_paths.get_annotated_filepath(video)
        if video_path is None:
            raise ValueError("Video file not found")

        # Get video info
        info = self._get_video_info(video_path)

        # Check if video duration is at least 5 seconds
        if info['duration'] < 5.0:
            raise ValueError("Video must be at least 5 seconds long")

        # Convert video to 24fps and read frames
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', video_path,
            '-vf', 'fps=fps=24',  # Force 24fps
            '-f', 'image2pipe',
            '-pix_fmt', 'rgb24',
            '-vcodec', 'rawvideo',
            '-'
        ]

        process = subprocess.Popen(ffmpeg_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        frames = []

        frame_size = info['width'] * info['height'] * 3

        while True:
            raw_frame = process.stdout.read(frame_size)
            if len(raw_frame) != frame_size:
                break

            frame = torch.frombuffer(raw_frame, dtype=torch.uint8)
            frame = frame.reshape(info['height'], info['width'], 3)
            frame = frame.float() / 255.0
            frames.append(frame)

        process.stdout.close()
        process.wait()

        if process.returncode != 0:
            raise RuntimeError(f"FFmpeg error: {process.stderr.read().decode()}")

        if len(frames) == 0:
            raise ValueError("No frames could be extracted from the video")

        video_info = (info['fps'], info['width'], info['height'], info['duration'])
        return (torch.stack(frames), video_info)


class PrepVideoForExtend:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "frames": ("IMAGE",),
                "cut_point": ("FLOAT", {"default": 0.0, "min": 0.0, "max": 1000.0, "step": 0.1}),
                "cut_point_type": (["seconds", "frames"], {"default": "seconds"}),
            }
        }

    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("processed_frames",)
    FUNCTION = "process_video"
    CATEGORY = "Klinter"

    def process_video(self, frames: torch.Tensor, cut_point: float, cut_point_type: str):
        """Process video frames for extension.
        
        Args:
            frames: Tensor of video frames
            cut_point: Point at which to cut the video
            cut_point_type: Whether cut_point is in seconds or frames
            
        Returns:
            Tensor of processed frames
        """
        num_frames = frames.shape[0]

        # Calculate frame positions
        if cut_point_type == "seconds":
            start_frame = int(cut_point * 24)  # Assuming 24fps from the import node
        else:
            start_frame = int(cut_point)

        frames_needed = 120  # 5 seconds at 24fps

        if start_frame + frames_needed > num_frames:
            raise ValueError("Cut point must leave at least 5 seconds of video")
        if num_frames < frames_needed:
            raise ValueError("Video must be at least 5 seconds long")

        selected_frames = frames[start_frame:start_frame + frames_needed]
        return (selected_frames,)
