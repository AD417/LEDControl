from aio_stdout import ainput, aprint
from rpi_ws281x import PixelStrip, Color
import asyncio
import concurrent.futures as cf
from types import SimpleNamespace
from internals.commands import *
from internals.command_handler import *
from internals.utils import try_num

# LED strip configuration:
LED_COUNT = 100        # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

Program = SimpleNamespace(**{
    # The LED array.
    "strip": PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL),
    # Whether the program is running.
    "running": True,
    # The intended interval.
    "real_interval": 1,
    # The interval we give asyncio Timeout to make up for commands taking a while to run.
    "interval": 1,
    # Current State:
    # 0: off
    # 1: fill
    # 2: alternating
    "state": 0,
    "color": (255,255,255),
    # Animation timer, used to determine where the program is in some process.
    "animation": 2,
    # Maximum of the animation timer.
    "max_animation": 3,

    # INTERRUPTS IN PROGRAM FLOW:
    # If the program's main loop is being interrupted (eg: by a flash.)
    "interrupt": False,
    "interrupt_state": 0,
    # Timer to indicate when normal execution resumes.
    "interrupt_timer": 0,

    # SPECIAL STUFF:
    # The color used when flashing the LEDs. 
    "flash_color": (255,0,63),
    # The last command used; used for recursion. 
    "last_command": "",
    # If "recursion" is enabled currently.
    "recursion": False,
    # the next command to execute after the interrupt ends.
    "next_command": "",
})

def update_state(): 
    fill(Program.strip, Color(0,0,0))

def on_frame():
    if Program.state == 0:
        fill(Program.strip, Color(0,0,0))
    elif Program.state == 1: 
        fill(Program.strip, Color(*Program.color))
    elif Program.state == 2:
        if Program.animation == 0: Program.animation = Program.max_animation
        Program.animation -= 1
        theaterChaseFrame(Program.strip, Color(*Program.color), Program)

async def on_interrupt(event):
    if Program.interrupt_state == 1:
        fill(Program.strip, Color(*Program.flash_color))
    # If interrupt is 0, then we simply pause. Free command!
    try: 
        await asyncio.wait_for(event.wait(), Program.interrupt_timer)
        event.clear()
    except (cf.TimeoutError, asyncio.TimeoutError): pass
    fill(Program.strip, Color(0,0,0))

async def get_input(command_executed_event: asyncio.Event): 
    while Program.running:
        try:
            full_command = (await ainput("$ ")).strip().lower()
        except KeyboardInterrupt: 
            # This except never seems to trigger. Ah well. 
            full_command = "exit"

        if Program.recursion:
            if full_command == "":
                full_command = Program.last_command
                await aprint("> Re-executing last command: " + full_command)
            else:
                Program.recursion = False
        
        await do_my_command(full_command, Program, command_executed_event)

async def led_loop(command_executed_event):
    while Program.running: 
        try: 
            await asyncio.wait_for(command_executed_event.wait(), Program.interval)
            command_executed_event.clear()
            # TODO: Add stuff that happens on these events. Maybe flashes of light?
            if not Program.interrupt: 
                update_state()
        except (cf.TimeoutError, asyncio.TimeoutError): pass

        # Eventually, other logic will be inserted here. 
        if Program.interrupt:
            await on_interrupt(command_executed_event)
            Program.interrupt = False
        on_frame()
    
    Program.running = False
    fill(Program.strip, Color(0,0,0))

async def main():
    Program.strip.begin()
    # This event syncs both sides of this operation. 
    # I probably should create a new "led_loop" task from the get_input function. 
    event = asyncio.Event()
    await asyncio.gather(led_loop(event), get_input(event))

if __name__ == "__main__":
    asyncio.run(main()) 