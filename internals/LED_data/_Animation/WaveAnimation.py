from __future__ import annotations
from .Animation import Animation
from ..RGB import RGB
import math

class WaveAnimation(Animation):
    """Continuous Alternating Animation. Creates a wave that ripples through an array at a set speed and wavelength. \n
    Parameters:
    `period`: the period of a single wave, in seconds. Note that this is *not* the same as the `frame_interval` for the alternating animation (Although it may be changed in the future).
    `wave_length`: the width of one wave. One wave is defined as the number of LED pixels between two fully lit pixels.Default 5.0; can be a noninteger value."""
    continuum = True
    def __init__(self: Animation, color: RGB = ..., period_sec: float = 1, wave_length: float = 5):
        super().__init__(color, period_sec / wave_length)
        self.wave_length = wave_length

    def pixel_state(self: WaveAnimation, pixel_id: int) -> RGB:
        frame = self.frame()
        fill_percentage = 0.5 * (1 - math.cos(2 * math.pi * (frame + pixel_id) / self.wave_length))
        return self.dark_led.interpolate(self.color, fill_percentage)