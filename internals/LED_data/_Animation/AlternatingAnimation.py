from __future__ import annotations

from .Animation import Animation
from datetime import timedelta
from ..RGB import RGB
from dataclasses import dataclass

@dataclass
class AlternatingAnimation(Animation):
    """Simple "Theater Chase" animation, based on the version used in "Chicago". Sets every `width`th pixel to be on, shifting the pixel used every `frame_interval` seconds. \n
    Parameters: 
    `frame_interval`: The amount of time between frames, or movements of the lit LEDs. Default 0.5s. Value must be at least 50ms. 
    `width`: How often a lit pixel appears in the array. Default 3. Minimum 2. If every `X`th LED is lit, then there are `X-1` unlit LEDs between them. """
    width: int = 3

    def pixel_state(self: AlternatingAnimation, pixel_id: int) -> RGB:
        frame = self.frame()
        if (frame + pixel_id) % self.width == 0: return self.color
        return self.dark_led
