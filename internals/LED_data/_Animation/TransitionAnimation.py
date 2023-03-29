from __future__ import annotations

from datetime import timedelta

from ..components import Animation, DeltaAnimation, RGBArray


class TransitionAnimation(DeltaAnimation):
    name: str = "Transition"

    def __init__(
            self: DeltaAnimation, 
            transition_time: timedelta, 
            current_animation: Animation, 
            future_animation: Animation
    ):
        super().__init__(transition_time, current_animation, future_animation, future_animation)

    def blend_strips(
            self: DeltaAnimation, 
            current_strip: RGBArray,
            interrupt_strip: RGBArray,
            future_strip: RGBArray, 
            transition_percentage: float
    ) -> RGBArray:
        return current_strip.interpolate(future_strip, transition_percentage)

    