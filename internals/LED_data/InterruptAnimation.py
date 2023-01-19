from __future__ import annotations

from .Animation import Animation
from .RGB import RGB
import time

class InterruptAnimation(Animation):
    interrupt = True
    overwrite = True
    def __init__(self: Animation, color: RGB = ..., timeout_sec: float = 0.5):
        super().__init__(color, 0)
        self.timeout_sec = timeout_sec
        self.end_time = self.start_time + timeout_sec

    def is_complete(self: InterruptAnimation) -> bool:
        return time.time() > self.end_time
    
    def interrupt_percentage(self: InterruptAnimation) -> float:
        time_since_start = self.start_time - time.time()
        return time_since_start / self.timeout_sec