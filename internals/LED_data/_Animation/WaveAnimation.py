from __future__ import annotations
from .Animation import Animation
from ..RGB import RGB
import math

class WaveAnimation(Animation):
    continuum = True
    kill_color = RGB(0,0,0)
    def __init__(self: Animation, color: RGB = ..., period_sec: float = 1, wave_length: float = 5):
        super().__init__(color, period_sec / wave_length)
        self.wave_length = wave_length

    def pixel_state(self: WaveAnimation, pixel_id: int) -> RGB:
        frame = self.frame()
        fill_percentage = 0.5 * (1 - math.cos(2 * math.pi * (frame + pixel_id) / self.wave_length))
        return self.kill_color.interpolate(self.color, fill_percentage)