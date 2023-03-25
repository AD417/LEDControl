from __future__ import annotations

import asyncio
from datetime import timedelta

from rpi_ws281x import PixelStrip, ws

from .LED_data import RGBArray, FireworkAnimation
from .command.handler import do_my_command
from . import Program

LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False

def from_pin(pin: int, led_count: int) -> PixelStrip:

    CHANNEL_ONE_PINS = [13, 19, 41, 45, 53]
    channel: int = 1 if pin in CHANNEL_ONE_PINS else 0

    return PixelStrip(
        led_count,
        pin,
        LED_FREQ_HZ,
        LED_DMA,
        LED_INVERT,
        LED_BRIGHTNESS,
        channel
    )

strips: dict[str, PixelStrip] = {
    "buildings": from_pin(18, 300),

    "left_firework": from_pin(10, 100),
    "middle_firework": from_pin(21, 100),
    "right_firework": from_pin(13, 100),
}

firework_animations: dict[str, FireworkAnimation] = {
    "left": FireworkAnimation(frame_interval=timedelta(milliseconds=30)),
    "middle": FireworkAnimation(frame_interval=timedelta(milliseconds=40)),
    "right": FireworkAnimation(frame_interval=timedelta(milliseconds=35))
}

def begin():
    """
    Initialize the ws281x library for all arrays. 
    Must be called before any updates can occur.
    """
    if Program.dry_run: return
    strips["buildings"].begin()
    strips["left_firework"].begin()
    strips["middle_firework"].begin()
    strips["right_firework"].begin()
    
def end():
    """Turn off all of the LED Arrays. Only to be used when the program is terminating!"""
    if Program.dry_run: return
    array = RGBArray(300)
    for strip_name in strips:
        array.send_output_to(strips[strip_name])
        strips[strip_name].show()

def interrupt(): ...

def reset_fireworks():
    for i in firework_animations:
        firework_animations[i].reset()

def update():
    """Update all of the strips, based on which ones should be enabled currently."""
    if Program.animation.is_complete():
        Program.is_interrupted = False
        Program.animation = Program.animation.next_animation()
        if Program.performing_next_command:
            Program.performing_next_command = False
            do_my_command(Program.next_command)

    if Program.dry_run:
        return
    
    fireworks = Program.active_strips & 0b111 == 0

    if fireworks:
        if isinstance(Program.animation, FireworkAnimation):
            left_array = firework_animations["left"].apply_to(RGBArray(100))
            left_array.send_output_to(strips["left_firework"])
            middle_array = firework_animations["middle"].apply_to(RGBArray(100))
            middle_array.send_output_to(strips["middle_firework"])
            right_array = firework_animations["right"].apply_to(RGBArray(100))
            right_array.send_output_to(strips["right_firework"])
            return
    

    RGBArray(100).send_output_to(strips["left_firework"])
    RGBArray(100).send_output_to(strips["middle_firework"])
    RGBArray(100).send_output_to(strips["right_firework"])

    left =      Program.active_strips & 0b001 > 0
    middle =    Program.active_strips & 0b010 > 0
    right =     Program.active_strips & 0b100 > 0


    array = RGBArray(300)
    array = Program.animation.apply_to(array)

    if not left:
        array.mask(0, 100)
    if not middle:
        array.mask(100, 200)
    if not right:
        array.mask(200, 300)
    array.send_output_to(strips["buildings"])
    strips["buildings"].show()
    

    # if fireworks:
    #     array.send_output_to(strips["fireworks"])
    # else:
    #     RGBArray(300).send_output_to(strips["fireworks"])
    # strips["fireworks"].show()