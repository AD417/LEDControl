from __future__ import annotations
from .Animation import Animation
from .RGB import RGB
import time
from typing import Any

class TransitionAnimation(Animation):
    continuum: bool = True
    def __init__(self: TransitionAnimation, color: RGB, transition_time_sec: float = 1, **config: Any):
        super().__init__(color, 0, config)
        self.transition_time_sec = transition_time_sec
        self.current_animation: Animation = config["current_animation"]
        self.future_animation: Animation = config["future_animation"]

    def transition_percentage(self: TransitionAnimation) -> int|float:
        """Determine how far we are through the transition."""
        time_since_start = time.time() - self.start_time
        return time_since_start / self.transition_time_sec

    def transition_complete(self: TransitionAnimation) -> bool:
        return self.transition_percentage() >= 1

    def new_animation(self: TransitionAnimation) -> Animation:
        return self.future_animation

    def pixel_state(self: TransitionAnimation, pixel_id: int) -> RGB:
        transition_percentage = self.transition_percentage()
        color1 = self.current_animation.pixel_state(pixel_id)
        color2 = self.future_animation.pixel_state(pixel_id)
        return color1.interpolate(color2, transition_percentage)