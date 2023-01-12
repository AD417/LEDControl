from aio_stdout import ainput, aprint
from rpi_ws281x import PixelStrip, Color
import asyncio
import concurrent.futures as cf
from types import SimpleNamespace
from internals.commands import *
from internals.utils import try_num

# LED strip configuration:
LED_COUNT = 100        # Number of LED pixels.
LED_PIN = 21          # GPIO pin connected to the pixels (18 uses PWM!).
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
    # When the program began.
    "start": time.time(),
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
})

def update_state(): ...

def on_frame():
    if Program.state == 0:
        fill(Program.strip, Color(0,0,0))
    elif Program.state == 1: 
        fill(Program.strip, Color(*Program.color))
    elif Program.state == 2:
        if Program.animation == 0: Program.animation = Program.max_animation
        Program.animation -= 1
        theaterChaseFrame(Program.strip, Color(*Program.color), Program)

async def get_input(event: asyncio.Event): 
    while Program.running:
        futureState = -1
        try:
            full_command = (await ainput("$ ")).strip()
        except KeyboardInterrupt: 
            # This except never seems to trigger. Ah well. 
            full_command = "exit"

        parameters = full_command.split(" ")
        command = parameters.pop(0)

        if command == "kill" or command == "off":
            futureState = 0
        elif command == "fill" or command == "on":
            futureState = 1
        elif command == "alt": 
            futureState = 2
            interval = 500
            width = 3
            if len(parameters) > 0:
                interval = try_num(parameters[0])
                if interval >= 50: 
                    Program.interval = interval * 0.001
                else: 
                    Program.interval = 0.5
            if len(parameters) > 1: 
                width = try_num(parameters[1])
                if width > 1: 
                    Program.max_animation = int(width)
                else: 
                    Program.max_animation = 3
            await aprint(
                f">   Alternating!\n    Interval: {interval}ms\n    Alt size: 1 in {width}"
            )
        elif command == "exit":
            Program.running = False
        else:
            await aprint("Invalid command: %s" % full_command)
            continue
            
        if futureState == Program.state: continue
        if futureState != -1:
            Program.state = futureState
            Program.same_cmd = False
        event.set()

async def led_loop(event):
    while Program.running:
        try: 
            await asyncio.wait_for(event.wait(), Program.interval)
            event.clear()
            # TODO: Add stuff that happens on these events. Maybe flashes of light?
            update_state()
        except (cf.TimeoutError, asyncio.TimeoutError):
            pass
        finally: 
            # Eventually, other logic will be inserted here. 
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