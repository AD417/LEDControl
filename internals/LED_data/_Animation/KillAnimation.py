from __future__ import annotations

from dataclasses import dataclass

from ..components import Animation, RGBArray

@dataclass
class KillAnimation(Animation):
    """Simple Kill Animation, which sets all the LEDs in the array to their darkest state, `RGB(0,0,0)` / Off. \n
    Parameters: None"""

    def apply_to(self: Animation, strip: RGBArray):
        for pixel in range(strip.size):
            strip[pixel] = self.dark_led
        
        return strip

    def __str__(self) -> str:
        out = ""
        out += "nothing.\n"
        
        return out