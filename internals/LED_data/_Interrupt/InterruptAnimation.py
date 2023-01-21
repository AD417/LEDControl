from __future__ import annotations

from .._Animation.Animation import Animation
from ..RGB import RGB
import time

class InterruptAnimation(Animation):
    """Abstract Interrupting Animation class for animations that interrupt normal program flow to display something to the LED array."""
    interrupt = True
    overwrite = True
    def __init__(self: Animation, color: RGB = ..., timeout_sec: float = 0.5):
        super().__init__(color)
        self.timeout_sec = timeout_sec
        self.end_time = self.start_time + timeout_sec

    def is_complete(self: InterruptAnimation) -> bool:
        return time.time() > self.end_time
    
    def interrupt_percentage(self: InterruptAnimation) -> float:
        """Determine how far we are through the interrupt.
        Returns: a decimal value between 0 and 1, includive, indicating percentage."""
        time_since_start = self.start_time - time.time()
        return time_since_start / self.timeout_sec