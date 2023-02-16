from __future__ import annotations

from dataclasses import dataclass

from .Animation import Animation
from ..RGB import RGB

@dataclass
class FillAnimation(Animation):
    """Simple Fill Animation, based on the version used in Chicago. Sets every single LED in the array to be the preset color, all the time. \n
    Parameters: None"""
    def pixel_state(self: FillAnimation, pixel_id: int) -> RGB:
        return self.color

    def __str__(self) -> str:
        out = ""
        out += "a Fill Animation.\n"
        
        return out