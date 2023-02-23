from __future__ import annotations

from dataclasses import dataclass

from ..components import RGB, RGBArray
from .InterruptAnimation import InterruptAnimation

@dataclass
class FlashAnimation(InterruptAnimation):
    """Interrupting Animation that overrides the LED array to flash a single color for a set interval. \n
    Parameters: 
    None"""

    def apply_to(self: FlashAnimation, strip: RGBArray):
        for pixel in range(strip.size):
            strip[pixel] = self.color
        return strip

    def __str__(self) -> str:
        out = ""
        out += "a Flash!\n"

        transition_time_ms = (self.end_time - self.start_time).total_seconds() * 1000

        if self.is_complete():
            out += "    This flash is complete.\n"
        else:
            out += "    This flash is %i%% complete. (Length: %ims)\n" \
                        % (self.interrupt_percentage() * 100, transition_time_ms)

        return out