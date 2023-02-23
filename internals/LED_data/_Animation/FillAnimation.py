from __future__ import annotations

from dataclasses import dataclass

from ..Components import Animation, RGB, RGBArray

@dataclass
class FillAnimation(Animation):
    """Simple Fill Animation, based on the version used in Chicago. Sets every single LED in the array to be the preset color, all the time. \n
    Parameters: None"""

    def apply_to(self: FillAnimation, strip: RGBArray):
        for pixel in range(strip.size):
            strip[pixel] = self.color
        
        return strip

    def pixel_state(self: FillAnimation, pixel_id: int) -> RGB:
        return self.color

    def __str__(self) -> str:
        out = ""
        out += "a Fill Animation.\n"
        
        return out