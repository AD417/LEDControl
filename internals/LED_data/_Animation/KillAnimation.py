from __future__ import annotations
from .Animation import Animation
from ..RGB import RGB

class KillAnimation(Animation):
    kill_color = RGB(0,0,0)
    def pixel_state(self: KillAnimation, pixel_id: int) -> RGB:
        return self.kill_color