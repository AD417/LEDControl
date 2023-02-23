from __future__ import annotations

from ..components import DeltaAnimation, RGBArray

class TransitionAnimation(DeltaAnimation):
    name: str = "Transition"

    def blend_strips(
            self: DeltaAnimation, 
            current_strip: RGBArray, 
            future_strip: RGBArray, 
            transition_percentage: float
    ) -> RGBArray:
        return current_strip.interpolate(future_strip, transition_percentage)

    