from __future__ import annotations
from .Animation import Animation
from ..RGB import RGB

class FillAnimation(Animation):
    def pixel_state(self: FillAnimation, pixel_id: int) -> RGB:
        return self.color