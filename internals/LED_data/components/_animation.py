from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from dataclasses import dataclass, field
from typing import ClassVar

from ._rgb import RGB
from ._rgb_array import RGBArray

@dataclass
class Animation(ABC):
    """Abstract Animation class for the creation of animations for an LED array. \n
    To use, derive this class and override / implement the `Animation.strip_state(pixel_id)` method."""
    continuum: ClassVar[bool] = False
    dark_led: ClassVar[RGB] = RGB(0,0,0)
    interrupt: ClassVar[bool] = False

    color: RGB = field(default=RGB(0,0,0))
    frame_interval: timedelta = field(default=timedelta(seconds=1))
    start_time: datetime = field(default_factory=datetime.now)

    from dataclasses import replace as copy

    def frame(self: Animation) -> int|float:
        """Determine the current frame of the animation, based on the time passed since the program began. \n
        If continuum is enabled, the value will be a continuous decimal. \n
        If continuum is disabled, the value will be a integer, rounded down to 0."""
        if self.frame_interval <= timedelta(): return 0
        frame: float = (datetime.now() - self.start_time) / self.frame_interval
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
    def apply_to(self: Animation, strip: RGBArray):
        """Apply this animation to an RGB array, given the animation type and amount of time since the animation began. \n
        Parameters:
        `strip`: The RGBArray to apply this animation to."""
        pass

    def __str__(self) -> str:
        """This Animation is..."""
        out = "an undocumented Animation: %r\n" % type(self)
        return out


if __name__ == "__main__":
    a = Animation(100) # Deliberate TypeError.