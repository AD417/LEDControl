from aio_stdout import ainput, aprint
from rpi_ws281x import PixelStrip, Color
import asyncio
import concurrent.futures as cf
from types import SimpleNamespace
from internals.command_handler import do_my_command
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
    # Whether the program is running.
    "is_running": True,
    # The current animation used by the strip
    "animation": KillAnimation(),

    "color": RGB(255,0,0),
    "is_interrupted": False,
    "interrupt": FlashAnimation(),

    "flash_color": RGB(255,255,255),
    "performing_recursion": False,
    "recursive_command": "",
    "next_command": "",
})

def on_frame():
    ARRAY.update_strip_using(Program.animation)
    ARRAY.send_output_to(STRIP)

def on_interrupt():
    if type(Program.interrupt) != PauseAnimation:
        ARRAY.update_strip_using(Program.interrupt)
        ARRAY.send_output_to(STRIP)
    
    if Program.interrupt.is_complete(): 
        Program.is_interrupted = False

async def get_input(): 
    while Program.is_running:
        try:
            full_command = (await ainput("$ ")).strip().lower()
        except KeyboardInterrupt: 
            # This except never seems to trigger. Ah well. 
            full_command = "exit"
        
        if full_command == "" and Program.performing_recursion:
            full_command = Program.recursive_command

        await do_my_command(full_command, Program)

async def led_loop():
    while Program.is_running: 
        if Program.is_interrupted:
            on_interrupt()
        else:
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