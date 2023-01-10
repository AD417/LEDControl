#!/usr/bin/env python3
# NeoPixel library strandtest example

from aio_stdout import ainput, aprint
from rpi_ws281x import PixelStrip, Color
import asyncio
import argparse
import time

# LED strip configuration:
LED_COUNT = 100        # Number of LED pixels.
LED_PIN = 21          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

class Timer:
    # When the program began.
    start = time.time()
    # When the LEDS changed last.
    last_delta = time.time()
    # When the LEDs are next set to change.
    next_delta = 0
    # How often the LEDs change, in secs.
    interval = 0.5
    # Whether the command has changed.
    same_cmd = False
    # Whether to stop everything.
    running = True
    # Current State:
    # 0: off
    # 1: fill
    # 2: alternating
    state = 2
    # Animation timer, used to determine where the program is in some process.
    animation = 2
    # Maximum of the animation timer.
    max_animation = 3

    def reset_interval_timer(new_interval: float = 0):
        Timer.interval = new_interval
        Timer.next_delta = time.time()
        Timer.last_delta = 0

    def set_next_delta():
        Timer.last_delta = Timer.next_delta
        Timer.next_delta = Timer.last_delta + Timer.interval
    
    def reset_animation(): 
        Timer.animation = Timer.max_animation - 1
    
    def tick_animation():
        if Timer.animation == 0: Timer.reset_animation()
        Timer.animation -= 1


# async def fill(strip, rgb, change_time=1000):
#     """Turn on every pixel in the display incrementally."""
#     Timer.interval = change_time / 256
#     Timer.last_delta = time.time()
#     for step in range(256):
#         Timer.set_next_delta()
#         for i in range(strip.numPixels()):
#             strip.setPixelColor(
#                 i,
#                 Color(*(int(x * step / 255) for x in rgb))
#             )

async def fill(strip, color):
    """Wipe color across display a pixel at a time, rapidly"""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()


async def theaterChaseFrame(strip, color):
    """Movie theater light style chaser animation."""
    Timer.tick_animation()
    for i in range(0, strip.numPixels(), 3):
        strip.setPixelColor(i + Timer.animation, color)
    strip.show()
    for i in range(0, strip.numPixels(), 3):
        strip.setPixelColor(i + Timer.animation, 0)

async def get_input():
    while Timer.running:
        futureState = -1
        try:
            command = await ainput("$ ")
        except KeyboardInterrupt: 
            command = "exit"
        if command == "kill":
            futureState = 0
        elif command == "fill" or command == "on":
            futureState = 1
        elif command == "alt": 
            futureState = 2
        elif command == "exit":
            Timer.running = False
        else:
            await aprint("Invalid command: %s" % command)
            continue
            
        if futureState == Timer.state: continue
        Timer.state = futureState
        Timer.same_cmd = False

async def run_leds():
    # Create NeoPixel object with appropriate configuration.
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    while Timer.running:
        if not Timer.same_cmd:
            Timer.reset_interval_timer()
            if Timer.state == 2:
                Timer.interval = 0.5
            else: 
                Timer.interval = 100000
    
        our_time = time.time()
        if our_time > Timer.next_delta:
            print(f"{Timer.next_delta} < {our_time}")
            Timer.set_next_delta()
            if Timer.state == 0:
                await fill(strip, Color(0,0,0))
            elif Timer.state == 1: 
                await fill(strip, Color(255,0,0))
            elif Timer.state == 2:
                await theaterChaseFrame(strip, Color(255,0,0))
        # Wait for a miniscule amount of time (5ms)
        await asyncio.sleep(0.005)
    
    await fill(strip, Color(0,0,0))

async def main():
    await asyncio.gather(get_input(), run_leds())

# Main program logic follows:
if __name__ == '__main__':
    asyncio.run(main())