from __future__ import annotations
from abc import ABCMeta, abstractmethod
from RGB import RGB
import time

class Animation(metaclass=ABCMeta):
    interrupt: bool = False
    def __init__(self: Animation, frame_interval_sec: float = 0):
        self.start_time: float = time.time()
        self.frame_interval_sec: float = frame_interval_sec

    def frame(self: Animation) -> int:
        if self.frame_interval <= 0: return 0
        return (time.time() - self.start_time) // self.frame_interval_sec

    @abstractmethod
    def pixel_state(self: Animation, pixel: int) -> RGB:
        pass


if __name__ == "__main__":
    a = Animation(100)