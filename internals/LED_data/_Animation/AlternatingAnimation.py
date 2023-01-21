from __future__ import annotations
from .Animation import Animation
from ..RGB import RGB
from typing import Any

class AlternatingAnimation(Animation):
    """Simple "Theater Chase" animation, based on the version used in "Chicago". Sets every `width`th pixel to be on, shifting the pixel used every `frame_interval` seconds. \n
    Parameters: 
    `frame_interval`: The amount of time between frames, or movements of the lit LEDs. Default 0.5s / 500ms. Value must be at least 0.05. 
    `width`: How often a lit pixel appears in the array. Default 3. Minimum 2. If every `X`th LED is lit, then there are `X-1` unlit LEDs between them. """
    def __init__(self: Animation, color: RGB, frame_interval_sec: float = 0.5, width: int = 3):
        super().__init__(color, frame_interval_sec)
        self.width = width

    def pixel_state(self: AlternatingAnimation, pixel_id: int) -> RGB:
        frame = self.frame()
        if (frame + pixel_id) % self.width == 0: return self.color
        return self.dark_led
