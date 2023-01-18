from __future__ import annotations
from abc import ABCMeta, abstractmethod
from RGB import RGB
import time
from typing import Any

class Animation(metaclass=ABCMeta):
    interrupt: bool = False
    continuum: bool = False
    def __init__(self: Animation, color: RGB, frame_interval_sec: float = 0, /, **config):
        self.color = color
        self.frame_interval_sec: float = frame_interval_sec
        self.start_time: float = time.time()

    def frame(self: Animation) -> int|float:
        """Determine the current frame of the animation, based on the time passed since the program began."""
        if self.frame_interval <= 0: return 0
        frame = (time.time() - self.start_time) / self.frame_interval_sec
        if self.continuum: return frame
        return int(frame)

    def update_color(self: Animation, new_color: RGB):
        self.color = new_color

    @abstractmethod
    def pixel_state(self: Animation, pixel_id: int) -> RGB:
        """Determine the current state of the given pixel_id, given the animation type and amount of time since the animation began.
        Parameters:
        `pixel_id`: The pixel_id on the strip that we are modifying."""
        pass


if __name__ == "__main__":
    a = Animation(100) # TypeError.