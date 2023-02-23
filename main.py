from __future__ import annotations

import argparse
import asyncio
from datetime import datetime
import os.path

from rpi_ws281x import PixelStrip
from aio_stdout import ainput

from internals.LED_data import *
from internals.command.handler import do_my_command
import internals.Program as Program
from internals.command.fileloader import load_file, load_next_command, file_summary

# LED strip configuration:
LED_COUNT = 100       # Number of LED pixels.
LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
# LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10          # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

ARRAY = RGBArray(LED_COUNT)

STRIP = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)

dry_run = False

async def on_frame():
    global ARRAY
    ARRAY = Program.animation.apply_to(ARRAY)
    # ARRAY.update_strip_using(Program.animation)
    if not dry_run: 
        ARRAY.send_output_to(STRIP)
    if Program.animation.is_complete():
        Program.animation = Program.animation.next_animation()

async def on_interrupt():
    global ARRAY
    ARRAY = Program.interrupt.apply_to(ARRAY)
    # ARRAY.update_strip_using(Program.interrupt)
    if not dry_run:
        ARRAY.send_output_to(STRIP)

    if Program.interrupt.is_complete(): 
        Program.is_interrupted = False
        if Program.performing_next_command:
            Program.performing_next_command = False
            do_my_command(Program.next_command)

async def get_input(): 
    print("\n$ ", end="")
    while Program.is_running:
        if Program.file_loaded:
            await asyncio.sleep(0.25)
        try:
            full_command = (await ainput()).strip().lower()
        except KeyboardInterrupt: 
            # This except never seems to trigger. Ah well. 
            full_command = "exit"
        
        if Program.performing_recursion:
            if full_command == "":
                full_command = Program.recursive_command
            else:
                print("Aborting recursion.")
                Program.performing_recursion = False

        if full_command == "":
            if Program.is_paused or Program.is_interrupted:
                Program.is_paused = False
                Program.is_interrupted = False
            elif Program.file_loaded:
                full_command = load_next_command()
            

        do_my_command(full_command)

async def led_loop():
    global ARRAY
    if not dry_run:
        STRIP.begin()
    while Program.is_running: 
        # Yield execution to the get_input asyncio loop, if necessary.
        await asyncio.sleep(0.001)
        if Program.is_paused: 
            if datetime.now() > Program.time_to_unpause:
                Program.is_paused = False
                if Program.performing_next_command:
                    do_my_command(Program.next_command)
            else:
                continue
        if Program.is_interrupted:
            await on_interrupt()
        else:
            await on_frame()

    if not dry_run:
        ARRAY = KillAnimation().apply_to(ARRAY)
        ARRAY.send_output_to(STRIP)

async def main():
    await asyncio.gather(led_loop(), get_input())

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d", "--dry-run",
        action="store_true",
        help="Initiate a 'dry run', meaning no data is ever sent to the LEDs."
    )
    parser.add_argument(
        "-e", "--execute",
        help="The path to a file to execute.",
    )
    args = parser.parse_args()
    dry_run = args.dry_run

    if args.execute:
        path_to_instructions = os.path.abspath(args.execute)
        load_file(path_to_instructions)

    # print("\n".join(Program.command_queue))

    startup_time = datetime.now()

    welcome_message = "LEDControl v0.2.0\n"
    welcome_message += "Program created by AD417. Software is in BETA: expect bugs!\n"
    welcome_message += startup_time.strftime("Last login: %a %b %d %H:%M:%S %Y\n")
    
    if args.execute:
        welcome_message += "\n"
        welcome_message += "This program is executing " + args.execute + "\n"
        welcome_message += file_summary()

    print(welcome_message)
    asyncio.run(main()) 