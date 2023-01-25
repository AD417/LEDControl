from __future__ import annotations

from dataclasses import dataclass
from .InterruptAnimation import InterruptAnimation
from ..RGB import RGB

@dataclass
class FlashAnimation(InterruptAnimation):
    """Interrupting Animation that overrides the LED array to flash a single color for a set interval. \n
    Parameters: 
    None"""
    def pixel_state(self: FlashAnimation, pixel_id: int) -> RGB:
        return self.color