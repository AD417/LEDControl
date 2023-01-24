from __future__ import annotations

from datetime import datetime, timedelta
from .._Animation.Animation import Animation
from ..RGB import RGB
from dataclasses import dataclass, field

@dataclass
class InterruptAnimation(Animation):
    """Abstract Interrupting Animation class for animations that interrupt normal program flow to display something to the LED array."""
    interrupt = True
    overwrite = True

    end_time: datetime = field(init=False)

    def __post_init__(self: InterruptAnimation):
        self.end_time: datetime = self.start_time + self.frame_interval

    def is_complete(self: InterruptAnimation) -> bool:
        return datetime.now() > self.end_time
    
    def interrupt_percentage(self: InterruptAnimation) -> float:
        """Determine how far we are through the interrupt.
        Returns: a decimal value between 0 and 1, includive, indicating percentage."""
        time_since_start: timedelta = datetime.now() - self.start_time
        return time_since_start / self.frame_interval