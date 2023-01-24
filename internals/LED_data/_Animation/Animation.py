from __future__ import annotations

from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from ..RGB import RGB
from typing import ClassVar
from dataclasses import dataclass, field

@dataclass
class Animation(ABC):
    """Abstract Animation class for the creation of animations for an LED array. \n
    To use, derive this class and override / implement the `Animation.pixel_state(pixel_id)` method."""
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
    def pixel_state(self: Animation, pixel_id: int) -> RGB:
        """Determine the current state of the given pixel_id, given the animation type and amount of time since the animation began. \n
        Parameters:
        `pixel_id`: The index of the pixel that we are modifying."""
        pass


if __name__ == "__main__":
    a = Animation(100) # Deliberate TypeError.