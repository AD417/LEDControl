from __future__ import annotations

from dataclasses import dataclass, field
# from datetime import datetime
import random

from ..components import Animation, RGB, RGBArray

@dataclass
class FireworkAnimation(Animation):
    """Firework Animation used by In The Heights for fireworks scenes. \n
    Parameters: 
    `frame_interval`: The amount of time to make the LEDs move 1 pixel. Value must be at least 10ms. 
    """
    # Technical details: this animation is effectively a sawtooth animation with a randomized interval. 
    @dataclass
    class Firework:
        """A single firework instance, used in the overarching Firework Animation."""
        def _random_tail_length():
            return 10 + 15 * random.random()
        
        birth_frame: float
        color: RGB = RGB(255,255,255)
        tail_length: float = field(init=False, default_factory=_random_tail_length)

    continuum = True
    fireworks: list[Firework] = field(
        init=False, 
        default_factory=lambda: []
    )

    def __post_init__(self: FireworkAnimation):
        self.fireworks.append(self.Firework(0, RGB.random_bright()))

    def generate_new_firework(self: FireworkAnimation):
        frame = self.frame()

        last_firework = self.fireworks[-1]
        probability_of_new_firework = (frame - (last_firework.birth_frame + last_firework.tail_length + 15)) / 10
        # TODO: Figure out how to make the logic work exponentially. Or just chain the fireworks together. 
        if probability_of_new_firework > random.random():
            self.fireworks.append(self.Firework(
                birth_frame = frame,
                color = RGB.random_bright()
            ))
        
    def prune_fireworks(self: FireworkAnimation):
        frame = self.frame()
        oldest_firework = self.fireworks[0]
        if frame - oldest_firework.birth_frame > 100: self.fireworks.pop(0)

    def update_fireworks(self: FireworkAnimation):
        self.generate_new_firework()
        self.prune_fireworks()


    def apply_to(self: FireworkAnimation, strip: RGBArray):
        self.update_fireworks()

        frame = self.frame()
        for firework in self.fireworks:
            absolute_position = frame - firework.birth_frame
            for i in range(int(firework.tail_length)):
                pixel_position = int(absolute_position - i)
                if pixel_position >= strip.size or pixel_position < 0: continue
                
                percent_dark = i / firework.tail_length
                pixel_color = firework.color.interpolate(self.dark_led, percent_dark)
                strip[pixel_position] = pixel_color
                
        return strip

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
