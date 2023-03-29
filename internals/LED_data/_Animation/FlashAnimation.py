from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from ..components import Animation, DeltaAnimation, RGB, RGBArray
from .FillAnimation import FillAnimation

@dataclass
class FlashAnimation(DeltaAnimation):
    """Interrupting Animation that overrides the LED array to flash a single color for a set interval. \n
    Parameters: 
    None"""

    def __init__(
            self: FlashAnimation, 
            color: RGB = RGB(0,0,0),
            transition_time: timedelta = timedelta(), 
            current_animation: Animation = FillAnimation(),
    ):
        super().__init__(
            transition_time = transition_time, 
            current_animation = current_animation, 
            interrupt_animation = FillAnimation(color = color),
            future_animation = current_animation
        )

    def blend_strips(
            self: DeltaAnimation, 
            current_strip: RGBArray, 
            interrupt_strip: RGBArray, 
            future_strip: RGBArray, 
            transition_percentage: float
    ) -> RGBArray:
        # "Blending" my ass.
        return interrupt_strip

    def update_color_to(self: DeltaAnimation, color: RGB):
        self.color = color
        self.interrupt_animation.update_color_to(color)

    def __str__(self) -> str:
        out = ""
        out += "a Flash!\n"

        transition_time_ms = (self.end_time - self.start_time).total_seconds() * 1000

        if self.is_complete():
            out += "    This flash is complete.\n"
        else:
            out += "    This flash is %i%% complete. (Length: %ims)\n" \
                        % (self.transition_percentage() * 100, transition_time_ms)

        return out