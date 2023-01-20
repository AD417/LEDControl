from __future__ import annotations
from .Animation import Animation
from .RGB import RGB
import time

class TransitionAnimation(Animation):
    continuum: bool = True
    def __init__(self: TransitionAnimation, transition_time_sec: float, 
            current_animation: Animation, future_animation: Animation):

        super().__init__(RGB(0,0,0), 0)
        self.transition_time_sec = transition_time_sec
        self.end_time = self.start_time + transition_time_sec
        self.current_animation: Animation = current_animation
        self.future_animation: Animation = future_animation

    def update_color_to(self: TransitionAnimation, color: RGB):
        self.future_animation.update_color_to(color)

    def transition_percentage(self: TransitionAnimation) -> float:
        """Determine how far we are through the transition."""
        time_since_start = time.time() - self.start_time
        return time_since_start / self.transition_time_sec

    def is_complete(self: TransitionAnimation) -> bool:
        return time.time() > self.end_time

    def next_animation(self: TransitionAnimation) -> Animation:
        return self.future_animation

    def pixel_state(self: TransitionAnimation, pixel_id: int) -> RGB:
        transition_percentage = self.transition_percentage()    
        color1 = self.current_animation.pixel_state(pixel_id)
        color2 = self.future_animation.pixel_state(pixel_id)
        # if pixel_id == 0: print(color1.interpolate(color2, transition_percentage))
        return color1.interpolate(color2, transition_percentage)