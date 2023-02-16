from __future__ import annotations

from dataclasses import dataclass
import math

from .Animation import Animation
from ..RGB import RGB

@dataclass
class PulseAnimation(Animation):
    """Continuous Pulsing Animation. Tests the continuous animation feature of the Animation base class. Sets all the LEDs in the array to the same color, but rapidly changes that color through a sine wave. \n
    Parameters:
    `cycle_length`: the length of a single pulse, in seconds. Default 3s. Must be at least 0.1s. \n
    Note: high-frequency pulsing have have adverse effects for people with epilipsy. Usage is not recommended."""
    continuum = True
    
    def pixel_state(self: PulseAnimation, pixel_id: int) -> RGB:
        frame = self.frame()
        fill_percentage = 0.5 * (1 - math.cos(2 * math.pi * frame))
        return self.dark_led.interpolate(self.color, fill_percentage)

    def __str__(self) -> str:
        out = ""
        out += "a Pulsating Animation.\n"
        out += "    The light pulses on/off every %ims\n" % (self.frame_interval.total_seconds() * 1000)

        return out