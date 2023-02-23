from __future__ import annotations

from dataclasses import dataclass
import math

from .Animation import Animation
from ..RGB import RGB
from ..RGBArray import RGBArray

@dataclass
class WaveAnimation(Animation):
    """Continuous Alternating Animation. Creates a wave that ripples through an array at a set speed and wavelength. \n
    Parameters:
    `period`: the period of a single wave, in seconds. Note that this is *not* the same as the `frame_interval` for the alternating animation (Although it may be changed in the future).
    `wave_length`: the width of one wave. One wave is defined as the number of LED pixels between two fully lit pixels.Default 5.0; can be a noninteger value."""
    continuum = True

    wave_length: float = 5.0

    def fill_percentage(self: WaveAnimation, offset: float):
        return 0.5 * (1 - math.cos(2 * math.pi * offset / self.wave_length))

    def apply_to(self: WaveAnimation, strip: RGBArray):
        # Generally, the wavelength will be a very divisible number; 
        # no need to do sine a hundred times.
        cache: dict[float:float] = {}

        frame = self.frame()
        for pixel in range(strip.size):
            offset = (pixel + frame) % self.wave_length
            if offset not in cache:
                wave_color = self.dark_led.interpolate(self.color, self.fill_percentage(offset))
                cache[offset] = wave_color

            strip[pixel] = cache[offset]

        return strip

    def pixel_state(self: WaveAnimation, pixel_id: int) -> RGB:
        frame = self.frame()
        fill_percentage = 0.5 * (1 - math.cos(2 * math.pi * (frame + pixel_id) / self.wave_length))
        return self.dark_led.interpolate(self.color, fill_percentage)

    def __str__(self) -> str:
        out = ""
        out += "a Wave Animation.\n"
        out += "    Each wave is %.1fpx long.\n" % self.wave_length
        out += "    The wave moves by 1 pixel every %ims" % (self.frame_interval.total_seconds() * 1000)

        return out