from __future__ import annotations
from abc import ABCMeta, abstractmethod
from ..RGB import RGB
import time
from typing import Any

class Animation(metaclass=ABCMeta):
    """Abstract Animation class for the creation of animations for an LED array. \n
    To use, derive this class and override / implement the `Animation.pixel_state(pixel_id)` method."""
    continuum: bool = False
    dark_led: RGB = RGB(0,0,0)
    interrupt: bool = False
    def __init__(self: Animation, color: RGB = RGB(0,0,0), frame_interval_sec: float = 0):
        self.color = color
        self.frame_interval_sec: float = frame_interval_sec
        self.start_time: float = time.time()

    def frame(self: Animation) -> int|float:
        """Determine the current frame of the animation, based on the time passed since the program began."""
        if self.frame_interval_sec <= 0: return 0
        frame = (time.time() - self.start_time) / self.frame_interval_sec
        if self.continuum: return frame
        return int(frame)

    def update_color_to(self: Animation, new_color: RGB):
        """Change the color used in this animation.
        Parameters:
        `new_color`: An RGB value containing the color that this animation is being updated to. """
        self.color = new_color

    def is_complete(self: Animation) -> bool:
        """If this animation is a transition or otherwise temporary, evaluate if the animation has completed."""
        return False

    def next_animation(self: Animation) -> Animation:
        """If this animation is a transition or otherwise temporary, evaluate what animation we should change to when we complete."""
        return self

    @abstractmethod
    def pixel_state(self: Animation, pixel_id: int) -> RGB:
        """Determine the current state of the given pixel_id, given the animation type and amount of time since the animation began. \n
        Parameters:
        `pixel_id`: The pixel_id on the strip that we are modifying."""
        pass


if __name__ == "__main__":
    a = Animation(100) # TypeError.