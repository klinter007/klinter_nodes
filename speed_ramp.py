import numpy as np
import torch
from scipy.interpolate import interp1d
from comfy_api.latest import io

class SpeedRampNode(io.ComfyNode):
    @classmethod
    def define_schema(cls) -> io.Schema:
        """Define the schema for the speed ramp node.
        
        Returns:
            io.Schema: Node schema with inputs and outputs
        """
        return io.Schema(
            node_id="SpeedRamp",
            display_name="Speed Ramp - klinter",
            category="video",
            description="Apply speed ramp effects to video frames",
            inputs=[
                io.Image.Input("frames"),
                io.Boolean.Input("use_preset", default=True),
                io.Combo.Input("preset_curve", options=["double_peak", "quad_burst"]),
                io.Int.Input("base_fps", default=30, min=1, max=120),
                io.Float.Input("speed_values", default=1.0, min=0.1, max=10.0),
            ],
            outputs=[
                io.Image.Output()
            ]
        )

    @classmethod
    def _create_speed_curve(cls, speeds, num_frames):
        x = np.linspace(0, 1, len(speeds))
        curve = interp1d(x, speeds, kind='cubic', bounds_error=False, fill_value=(speeds[0], speeds[-1]))
        return curve(np.linspace(0, 1, num_frames))

    @classmethod
    def execute(cls, frames, use_preset, preset_curve, base_fps, speed_values) -> io.NodeOutput:
        # Convert frames to tensor if it isn't already
        if not isinstance(frames, torch.Tensor):
            frames = torch.stack(frames)
        
        # Store original frame order for validation
        frame_indices = np.arange(len(frames))
        
        # Get speed curve values
        if use_preset:
            if preset_curve == "double_peak":
                speeds = [1.0, 1.0, 1.2, 1.5, 1.8, 2.0, 2.0, 2.0, 2.0, 1.8, 1.5, 1.2, 1.0, 1.0]
            else:  # quad_burst
                speeds = [1.0, 1.0, 1.5, 2.5, 3.5, 4.0, 4.0, 4.0, 3.5, 2.5, 1.5, 1.0, 1.0]
        else:
            speeds = speed_values if isinstance(speed_values, (list, np.ndarray)) else [speed_values]
        
        # Calculate new frame positions
        total_frames = len(frames)
        frame_speeds = cls._create_speed_curve(speeds, total_frames)
        
        # Calculate cumulative time
        cumulative_time = np.cumsum(1.0 / frame_speeds)
        cumulative_time = cumulative_time / cumulative_time[-1]
        
        # Create frame mapping
        inverse_map = interp1d(cumulative_time, frame_indices, 
                             kind='linear',  # Changed to linear to prevent temporal artifacts
                             bounds_error=False, 
                             fill_value="extrapolate")
        
        # Calculate new frame positions
        new_positions = inverse_map(np.linspace(0, 1, total_frames))
        new_positions = np.clip(new_positions, 0, total_frames - 1).astype(int)
        
        # Print some debug info
        print(f"First few frame mappings: {new_positions[:10]}")
        print(f"Speed curve sample: {frame_speeds[:10]}")
        
        # Create new tensor with proper temporal order
        new_frames = torch.stack([frames[i] for i in new_positions])
        
        return io.NodeOutput(new_frames)
