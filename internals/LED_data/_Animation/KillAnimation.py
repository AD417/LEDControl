from __future__ import annotations

from .Animation import Animation
from ..RGB import RGB

class KillAnimation(Animation):
    """Simple Kill Animation, which sets all the LEDs in the array to their darkest state, `RGB(0,0,0)` / Off. \n
    Parameters: None"""
    def pixel_state(self: KillAnimation, pixel_id: int) -> RGB:
        return self.dark_led