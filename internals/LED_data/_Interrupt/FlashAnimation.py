from __future__ import annotations
from .InterruptAnimation import InterruptAnimation
from ..RGB import RGB

class FlashAnimation(InterruptAnimation):
    """Interrupting Animation that overrides the LED array to flash a single color for a set interval. \n
    Parameters: 
    None"""
    def pixel_state(self: FlashAnimation, pixel_id: int) -> RGB:
        return self.color