from aio_stdout import ainput, aprint
from rpi_ws281x import PixelStrip, Color
import asyncio
import concurrent.futures as cf
from types import SimpleNamespace
from internals.commands import *
from internals.command_handler import *
from internals.LED_data import *


# LED strip configuration:
LED_COUNT = 100        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

ARRAY = RGBArray(LED_COUNT)

STRIP = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
STRIP.begin()

# """Handles general switching in program flow."""
Program = SimpleNamespace(**{
    # The LED array.
    "strip": PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL),
    # Whether the program is running.
    "running": True,
    # The current animation used by the strip
    "animation": KillAnimation(),

    "color": RGB(255,0,0),
    "interrupt": False
})

def on_frame():
    ARRAY.update_strip_using(Program.animation)
    ARRAY.send_output_to(STRIP)

async def on_interrupt(event):
    if Program.interrupt_state == 1:
        fill(Program.strip, Color(*Program.flash_color))
    # If interrupt is 0, then we simply pause. Free command!
    try: 
        await asyncio.wait_for(event.wait(), Program.interrupt_timer)
        event.clear()
    except (cf.TimeoutError, asyncio.TimeoutError): pass
    fill(Program.strip, Color(0,0,0))
    if Program.next_command != "":
        # Not sure why this line is needed. But it does. But it's probably better. 
        cmd = Program.next_command
        Program.next_command = ""
        await do_my_command(cmd, Program, event)

async def get_input(): 
    while Program.running:
        try:
            full_command = (await ainput("$ ")).strip().lower()
        except KeyboardInterrupt: 
            # This except never seems to trigger. Ah well. 
            full_command = "exit"
        
        await do_my_command(full_command, Program)

async def led_loop():
    while Program.running: 
        on_frame()
        # Yield execution to the get_input asyncio loop, if necessary.
        # Python cannot parallel process, unfortunately. 
        await asyncio.sleep(0.001)

    ARRAY.update_strip_using(KillAnimation())
    ARRAY.send_output_to(STRIP)

async def main():
    print("HELLO WORLD!")
    await asyncio.gather(led_loop(), get_input())

if __name__ == "__main__":
    asyncio.run(main()) 