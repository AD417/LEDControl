from __future__ import annotations
from .InterruptAnimation import InterruptAnimation
from .RGB import RGB

class FlashAnimation(InterruptAnimation):
    def pixel_state(self: FlashAnimation, pixel_id: int) -> RGB:
        return self.color