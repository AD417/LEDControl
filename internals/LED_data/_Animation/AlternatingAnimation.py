from __future__ import annotations

from dataclasses import dataclass

from ..Components import Animation, RGB, RGBArray

@dataclass
class AlternatingAnimation(Animation):
    """Simple "Theater Chase" animation, based on the version used in "Chicago". Sets every `width`th pixel to be on, shifting the pixel used every `frame_interval` seconds. \n
    Parameters: 
    `frame_interval`: The amount of time between frames, or movements of the lit LEDs. Default 0.5s. Value must be at least 50ms. 
    `width`: How often a lit pixel appears in the array. Default 3. Minimum 2. If every `X`th LED is lit, then there are `X-1` unlit LEDs between them. """
    width: int = 3

    def apply_to(self: AlternatingAnimation, strip: RGBArray):
        frame = self.frame()
        for pixel in range(strip.size):
            if (pixel + frame) % self.width == 0:
                strip[pixel] = self.color
            else:
                strip[pixel] = self.dark_led

        return strip

    def pixel_state(self: AlternatingAnimation, pixel_id: int) -> RGB:
        frame = self.frame()
        if (frame + pixel_id) % self.width == 0: return self.color
        return self.dark_led

    def __str__(self) -> str:
        ordinal = ""
        if self.width == 2: ordinal = "nd"
        elif self.width == 3: ordinal = "rd"
        else: ordinal = "th"
        out = ""
        out += "an Alternating Animation. \n"
        out += "    Every %i%s pixel is lit.\n" % (self.width, ordinal)
        out += "    This shifts every %ims\n" % (self.frame_interval.total_seconds() * 1000)
        
        return out
