from __future__ import annotations
from .Animation import Animation
from ..RGB import RGB
import math

class PulseAnimation(Animation):
    continuum = True
    kill_color = RGB(0,0,0)
    def __init__(self: Animation, color: RGB = ..., frame_interval_sec: float = 3):
        super().__init__(color, frame_interval_sec)
    def pixel_state(self: PulseAnimation, pixel_id: int) -> RGB:
        frame = self.frame()
        fill_percentage = 0.5 * (1 - math.cos(2 * math.pi * frame))
        return self.kill_color.interpolate(self.color, fill_percentage)