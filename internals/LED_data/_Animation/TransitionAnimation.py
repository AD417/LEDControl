from __future__ import annotations

from datetime import datetime, timedelta

from .Animation import Animation
from ..RGB import RGB

class TransitionAnimation(Animation):
    """Temporary, Continuous Animation used to shift between two otherwise incongruent animations in a smooth manner.
    Parameters: 
    `transition_time`: The amount of time over which the animation performs its transition, in seconds. Required. 
    `current_animation`: The animation we are transitioning from; the current animation. At 0% transition percentage, it is fully shown and washes out the final animation.
    `future_animation`: The animation we are transitioning to; the next animation. At 100% transition percentage, it is fully shown and washes out the initial animation."""
    continuum: bool = True
    def __init__(self: TransitionAnimation, transition_time: timedelta, 
            current_animation: Animation, future_animation: Animation):

        super().__init__()
        self.transition_time: timedelta = transition_time
        self.end_time: datetime = self.start_time + transition_time
        self.current_animation: Animation = current_animation
        self.future_animation: Animation = future_animation

    def update_color_to(self: TransitionAnimation, color: RGB):
        # We only need to update the future color!
        self.future_animation.update_color_to(color)

    def transition_percentage(self: TransitionAnimation) -> float:
        """Determine how far we are through the transition. 
        Returns: a decimal value between 0 and 1 inclusive, indicating percentage."""
        time_since_start: timedelta = datetime.now() - self.start_time
        return time_since_start / self.transition_time

    def is_complete(self: TransitionAnimation) -> bool:
        return datetime.now() > self.end_time

    def next_animation(self: TransitionAnimation) -> Animation:
        return self.future_animation

    def pixel_state(self: TransitionAnimation, pixel_id: int) -> RGB:
        transition_percentage = self.transition_percentage()    
        color1 = self.current_animation.pixel_state(pixel_id)
        color2 = self.future_animation.pixel_state(pixel_id)
        return color1.interpolate(color2, transition_percentage)
    
    def __str__(self) -> str:
        out = ""
        out += "a Transition Animation.\n"
        out += "    Currently:"

        current_animation_str = str(self.current_animation)
        for i, line in enumerate(current_animation_str.splitlines()):
            if i != 0:
                out += "    "
            out += line + "\n"
        
        out += "\n    Up next: "

        future_animation_str = str(self.future_animation)
        for i, line in enumerate(future_animation_str.splitlines()):
            if i != 0:
                out += "    "
            out += line + "\n"

        transition_time_ms = (self.end_time - self.start_time).total_seconds() * 1000

        if self.is_complete():
            out += "    This animation is complete.\n"
        else:
            out += "    This animation is %i%% through the %ims transition.\n" \
                        % (self.transition_percentage() * 100, transition_time_ms)

        return out
        