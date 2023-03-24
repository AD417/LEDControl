from __future__ import annotations

import asyncio

from rpi_ws281x import PixelStrip, ws

from internals.LED_data import RGBArray
from . import Program

LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False

STRIP_LED_COUNT = 100
FIREWORK_LED_COUNT = 60 # TODO: CHECK THIS!

def from_pin(pin: int, is_strip: bool) -> PixelStrip:
    pixels = STRIP_LED_COUNT if is_strip else FIREWORK_LED_COUNT

    CHANNEL_ONE_PINS = [13, 19, 41, 45, 53]
    channel: int = 1 if pin in CHANNEL_ONE_PINS else 0

    return PixelStrip(
        pixels,
        pin,
        LED_FREQ_HZ,
        LED_DMA,
        LED_INVERT,
        LED_BRIGHTNESS,
        channel
    )

strips: dict[str, PixelStrip] = {
    "left_strip": from_pin(18, True),
    "middle_strip": from_pin(13, True),
    "right_strip": from_pin(21, True), # 13 and 19 are the same?

    # XXX: Incorrectly allocated. FIX THIS!
    "fireworks": from_pin(10, False),
    # "middle_firework": from_pin(999, False),
    # "right_firework": from_pin(999, False),
}

def begin():
    """
    Initialize the ws281x library for all arrays. 
    Must be called before any updates can occur.
    """
    if Program.dry_run: return
    strips["left_strip"].begin()
    strips["middle_strip"].begin()
    strips["right_strip"].begin()
    strips["fireworks"].begin()
    
def end():
    """Turn off all of the LED Arrays. Only to be used when the program is terminating!"""
    if Program.dry_run: return
    array = RGBArray(100)
    for strip_name in strips:
        array.send_output_to(strips[strip_name])
        strips[strip_name].show()

def interrupt(): ...

def update():
    """Update all of the strips, based on which ones should be enabled currently."""
    if Program.animation.is_complete():
        Program.animation = Program.animation.next_animation()

    if Program.dry_run:
        return
    
    left =      Program.active_strips & 0b001 > 0
    middle =    Program.active_strips & 0b010 > 0
    right =     Program.active_strips & 0b100 > 0

    fireworks = Program.active_strips & 0b111 == 0

    array = RGBArray(100)
    array = Program.animation.apply_to(array)

    # XXX: arrays that are not enabled will not be updated! Pixels may be left on!
    if left:
        array.send_output_to(strips["left_strip"])
    else:
        RGBArray(100).send_output_to(strips["left_strip"])
    strips["left_strip"].show()
    if middle:
        array.send_output_to(strips["middle_strip"])
    else:
        RGBArray(100).send_output_to(strips["middle_strip"])
    strips["middle_strip"].show()
    if right:
        array.send_output_to(strips["right_strip"])
    else:
        RGBArray(100).send_output_to(strips["right_strip"])
    strips["right_strip"].show()
    

    if fireworks:
        array.send_output_to(strips["fireworks"])
    else:
        RGBArray(100).send_output_to(strips["fireworks"])
    strips["fireworks"].show()