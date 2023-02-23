from __future__ import annotations

from dataclasses import dataclass, field
from datetime import timedelta
import random

from .Animation import Animation
from ..RGB import RGB
from ..RGBArray import RGBArray

@dataclass
class TrafficAnimation(Animation):
    """Traffic Animation, based on concepts for "In the Heights" effects. 
    Creates 2 arrays of booleans that move in opposite directions, cooresponding to car headlights on a distant road. `True` boolean values coorespond to car headlights. They move by 1 unit per frame along their path, until they reach the end and get removed. \n
    Parameters:
    `frame_interval`: the time between frames, in seconds. Default `0.3s` / `300ms`.
    `road_size`: The length of the road / maximum LED id for the animation, for space reasons. Default `100`.
    `traffic_density`: The percentage of road spaces occupied by "cars". Default `0.1` / `10%`. Range from 0 to 1, inclusive. High percentages (above 50%) may ruin the effect."""

    frame_interval: timedelta = timedelta(milliseconds=300)
    road_size: int = 100
    traffic_density: float = 0.1
    eastbound: list[bool] = field(default_factory=list, init=False, repr=False)
    westbound: list[bool] = field(default_factory=list, init=False, repr=False)
    last_updated_frame: int = field(default=0, init=False)

    def __post_init__(self):
        for _ in range(self.road_size):
            self.eastbound.append(self.new_car())
            self.westbound.append(self.new_car())

    def new_car(self: TrafficAnimation) -> bool:
        """Use the traffic density to determine if a new car should be spawned at the beginning of a road.
        Returns: a boolean value indicating if a car should be spawned."""
        return random.random() < self.traffic_density

    def apply_to(self: TrafficAnimation, strip: RGBArray):
        if self.last_updated_frame != self.frame():
            self.eastbound = [self.new_car()] + self.eastbound[:-1]
            self.westbound = self.westbound[1:] + [self.new_car()]
            self.last_updated_frame = self.frame()
        
        pixels_to_display = min(self.road_size, strip.size)
        
        for pixel in range(pixels_to_display):
            if self.westbound[pixel] or self.eastbound[pixel]:
                strip[pixel] = self.color
            else:
                strip[pixel] = self.dark_led

        return strip


    def pixel_state(self: TrafficAnimation, pixel_id: int) -> RGB:
        # This is honestly a massive flaw. I want to rewrite the program so the entire strip is passed to the Animation, instead of doing it pixel by pixel. 
        if pixel_id >= self.road_size: return self.dark_led

        if self.last_updated_frame != self.frame() and pixel_id == 0:
            self.eastbound = [self.new_car()] + self.eastbound[:-1]
            self.westbound = self.westbound[1:] + [self.new_car()]
            self.last_updated_frame = self.frame()
        
        if self.westbound[pixel_id] or self.eastbound[pixel_id]:
            return self.color
        return self.dark_led

    def __str__(self) -> str:
        out = ""
        out += "a Traffic Animation.\n"
        out += "    The 'cars' in the animation move every %ims.\n" % (self.frame_interval.total_seconds() * 1000)
        out += "    About %.1f%% of the road is occupied by cars at any given time.\n" % (self.traffic_density * 100)
        
        return out