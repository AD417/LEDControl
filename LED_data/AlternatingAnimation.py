from __future__ import annotations
from Animation import Animation
from RGB import RGB
from typing import Any

class AlternatingAnimation(Animation):
    def __init__(self: Animation, color: RGB, frame_interval_sec: float = 0, /, **config: Any):
        super().__init__(color, frame_interval_sec, config)
        self.width = config["width"]

    kill_color = RGB(0,0,0)
    def pixel_state(self: AlternatingAnimation, pixel_id: int) -> RGB:
        frame = self.frame()
        if (frame + pixel_id) % self.width == 0: return self.color
        return self.kill_color