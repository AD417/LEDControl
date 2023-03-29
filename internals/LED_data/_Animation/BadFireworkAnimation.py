from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta
import math

from ..components import Animation, RGB, RGBArray

@dataclass
class FireworkAnimation(Animation):
    """Continuous Alternating Animation. Creates a wave that ripples through an array at a set speed and wavelength. \n
    Parameters:
    `period`: the period of a single wave, in seconds. Note that this is *not* the same as the `frame_interval` for the alternating animation (Although it may be changed in the future).
    `wave_length`: the width of one wave. One wave is defined as the number of LED pixels between two fully lit pixels.Default 5.0; can be a noninteger value."""
    continuum = True

    frame_interval = timedelta(milliseconds=100)

    firework_size: float = 10.0
    firework_spacing: float = 30.0
    firework_positions: list[float] = field(default_factory=lambda: [0.0])
    last_frame: float = field(init=False, default=0.0)

    def move_fireworks(self: FireworkAnimation):
        frame = self.frame()
        
        firework_made_this_frame = (int(self.last_frame) % self.firework_spacing == 0)
        firework_should_be_made = (int(frame) % self.firework_spacing == 0)
        if not firework_made_this_frame and firework_should_be_made:
            self.firework_positions.append(0)

        for i in range(len(self.firework_positions)):
            self.firework_positions[i] += frame - self.last_frame
        
        self.last_frame = frame

        if self.firework_positions[0] > 100:
            self.firework_positions.pop(0)

    # def fill_percentage(self: WaveAnimation, offset: float):
    #     return 0.5 * (1 - math.cos(2 * math.pi * offset / self.wave_length))

    def apply_to(self: FireworkAnimation, strip: RGBArray):
        # Generally, the wavelength will be a very divisible number; 
        # no need to do sine a hundred times.
        self.move_fireworks()

        for pixel in range(strip.size):
            potentially_relevant_fireworks = [x for x in self.firework_positions if x > pixel]
            if len(potentially_relevant_fireworks) == 0: break

            relevant_firework = min(potentially_relevant_fireworks)
            if relevant_firework - pixel > self.firework_size: continue

            dark_percentage = (relevant_firework - pixel) / self.firework_size

            pixel_color = self.color.interpolate(self.dark_led, dark_percentage)
            # print(pixel_color)

            strip[pixel] = pixel_color
            '''
            offset = (pixel + frame) % self.wave_length
            if offset not in cache:
                wave_color = self.dark_led.interpolate(self.color, self.fill_percentage(offset))
                cache[offset] = wave_color

            strip[pixel] = cache[offset]
            '''

        return strip

    def __str__(self) -> str:
        out = ""
        out += "The Fireworks!\n"
        out += "    Each firework is %.1fpx long.\n" % self.firework_size
        out += "    The wave moves by 1 pixel every %ims" % (self.frame_interval.total_seconds() * 1000)

        return out