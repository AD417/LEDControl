from __future__ import annotations

from aio_stdout import ainput, aprint
import asyncio
from .utils import try_num
from .color import try_get_color

async def do_my_command(full_command: str, Program, command_executed_event: asyncio.Event):
    """Execute a command providded by the user.\n
    Valid commands / basic info: 
    `kill` / `off`: Kill the lights
    `fill` / `on`: Turn on all lights
    `flash`: INTERRUPT: Flash the lights for an interval.
    `alt`: Make the lights alternate, akin to a theater chase.
    `color`: Set the color of the lights.
    `pause`: INTERRUPT: pause the lights for an interval.
    `exit`: Immediately shut down and exit the application."""
    parameters = full_command.split(" ")
    command = parameters.pop(0)

    if command == "kill" or command == "off":
        parameters = await kill_command(parameters, Program)
    elif command == "fill" or command == "on":
        parameters = await fill_command(parameters, Program)
    elif command == "flash":
        parameters = await flash_command(parameters, Program)
    elif command == "alt": 
        parameters = await alt_command(parameters, Program)
    elif command == "color":
        parameters = await color_command(parameters, Program)
    elif command == "pause":
        parameters = await pause_command(parameters, Program)
    elif command == "exit":
        Program.running = False
    else:
        if Program.interrupt and command == "":
            await aprint(">   Unpausing!")
            command_executed_event.set()
        else:
            await aprint("Invalid command: %s" % full_command)
        return

    while len(parameters) > 0:
        # Color command.
        if parameters[0] == "-c":
            parameters = await color_command(parameters[1:], Program)
        # Recursion parameter. 
        elif parameters[0] == "-e":
            Program.last_command = full_command
            if Program.recursion:
                await aprint("    Recursion continues. Type anything to break.")
            else:
                await aprint("    Initiating Recursion mode. Hit enter with a blank input to repeat last command.")
            Program.recursion = True
            # Most parameters are, by design, only ever the last parameter.
            break
        elif parameters[0] == "-k": 
            break
        elif parameters[0] == "-n":
            if not Program.interrupt:
                await aprint(f"""Error processing command args: "next" parameter cannot be used with {repr(command)} """)
                break
            break
        elif parameters[0] == "-p":
            parameters = await pause_command(parameters[1:], Program)
            break
        else: 
            await aprint("Error processing command args: '%s' is not a valid parameter." % parameters[0])
            break
    command_executed_event.set()


async def alt_command(parameters: list[str], Program):
    """
    Set the state of the LEDs to alternate in a theater chase.\n
    Legal parameters:
    `Interval`: The amount of time between frames while alternating, in milliseconds. Default 500. Value must be at least 50.
    `Width`: The frequency of lit pixels, in terms of the number of LEDs between Lit pixels. Default 3. Value must be at least 2."""
    Program.interrupt = False
    Program.state = 2
    interval_ms = 500
    width = 3
    used_params = 0

    if len(parameters) > 0:
        interval_ms = try_num(parameters[0])
    if interval_ms >= 50: 
        Program.interval = interval_ms * 0.001
        used_params = 1
    else: 
        Program.interval = 0.5

    if used_params == 1 and len(parameters) > 1: 
        width = try_num(parameters[1])
    if width > 1: 
        Program.max_animation = int(width)
        used_params = 2
    else: 
        Program.max_animation = 3

    await aprint(">   Theather Chase time!")
    await aprint(f"    Alternates every {int(1000 * Program.interval)}ms")
    await aprint(f"    1 in {int(Program.max_animation)} LEDs is lit.")

    return parameters[used_params:]

async def color_command(parameters: list[str], Program):
    """
    Set the color used by the animation. \n
    Legal parameters:
    `color`: The name of the color being used. Required. Value can be a single letter.
    Note: if the keyword "custom" or "c" is supplied, a valid RGB value must also be supplied. See :func:`custom_color_command` for more information."""
    if len(parameters) == 0: 
        await aprint(">   ERROR: Color command must supply a parameter!")
        return parameters
    if parameters[0] == "custom" or parameters[0] == "c": 
        return await custom_color_command(parameters, Program)
    success, color = try_get_color(parameters[0])
    if not success: 
        await aprint("""ERROR: "%s" is not a valid color!""" % parameters[0])
        return parameters
    
    if Program.interrupt: 
        Program.flash_color = color
        await aprint(">   Flash color has been changed to: " + parameters[0])
    else: 
        Program.color = color
        await aprint(">   Primary color has been changed to: " + parameters[0])
    return parameters[1:]

async def custom_color_command(parameters: list[str], Program):
    """
    Set a custom color used by the animation. \n
    Legal parameters:
    `R`: The level of Red. Required. Must be an integer between 0 and 255, inclusive.
    `G`: The level of Blue. Required. Must be an integer between 0 and 255, inclusive.
    `B`: The level of Green. Required. Must be an integer between 0 and 255, inclusive.
    """
    if len(parameters) < 4:
        await aprint(">   ERROR: Custom color must supply 3 numeric parameters.")
        return parameters[1:]
    try:
        r = int(parameters[1])
        g = int(parameters[2])
        b = int(parameters[3])
    except:
        await aprint(">   ERROR: Values are not all ints: %s, %s, %s" % tuple(parameters[1:4]))
        return parameters[4:]
    if max(r,g,b) > 255 or min(r,g,b) < 0:
        await aprint(">   ERROR: Value out of range: %s %s %s" % tuple(parameters[1:4]))
        return parameters[4:]
    if Program.interrupt:
        Program.flash_color = (r,g,b)
        await aprint(">   Flash color changed to a custom color: RGB(%s, %s, %s)" % tuple(parameters[1:4]))
    else:
        Program.color = (r,g,b)
        await aprint(">   Primary color changed to a custom color: RGB(%s, %s, %s)" % tuple(parameters[1:4]))
    return parameters[4:]

async def fill_command(parameters: list[str], Program):
    """Fill the lights with a single color.\n
    Legal Parameters:
    None"""
    Program.interrupt = False
    Program.state = 1
    # TODO: Fadein animation data

    await aprint(">   Lights on!")
    return parameters

async def flash_command(parameters: list[str], Program):
    """INTERRUPT: Override the current state of the lights and flash a color. This color may be different from the base color used by the rest of the program.\n
    Legal Parameters:
    `flash_time_ms`: The amount of time that the program spends in this flash state, in milliseconds. Default 1000ms. Must be greater than 0."""
    Program.interrupt = True
    await aprint(">   Flashing!")
    Program.interrupt_state = 1
    if len(parameters) == 0: 
        Program.interrupt_timer = 1
        await aprint("    For: 1000ms")
        return parameters
    
    flash_time_ms = try_num(parameters[0])
    if flash_time_ms <= 0: flash_time_ms = 1000
    Program.interrupt_timer = flash_time_ms * 0.001
    await aprint("    For: %sms" % int(flash_time_ms))
    return parameters[1:]

async def kill_command(parameters: list[str], Program):
    """Completely disable the lights, setting all pixels to `RGB(0,0,0)` (black).\n
    Legal Parameters:
    None"""
    Program.interrupt = False
    Program.state = 0
    # TODO: Fadeout animation data

    await aprint(">   Killing the lights!")
    return parameters

async def next_command(parameters: list[str], Program):
    """Set the command that executes immediately after the pending interrupt. (Interrupts are signified by `INTERRUPT` in the documentation."""
    ... # TODO

async def pause_command(parameters: list[str], Program):
    """INTERRUPT: Halt all execution. This halt may be either indefinite or for a set interval, based on supplied parameters.
    Legal Parameters:
    `pause_time_ms`: The amount of time to pause, in milliseconds. Default Infinity. Must be at least 50ms.\n
    Note: entering any command (or pressing the enter key) while the program is paused will immediately unpause. This is intended to aid in timing events with highly variable run time."""
    Program.interrupt = True
    Program.interrupt_state = 0
    # TODO: Test this code's interaction with flash. Pause on a flash could work with this, but would be super scuffed!
    if len(parameters) == 0:
        # An arbitrarily large number. 
        Program.interrupt_timer = 100000
        await aprint(">   Paused!")
        return [] # parameters
    pause_time_ms = try_num(parameters[0])
    if pause_time_ms < 50:
        await aprint(">   Paused! (Expected parameter 'time' not valid)")
        Program.interrupt_timer = 100000
        return parameters
    Program.interrupt_timer = pause_time_ms * 0.001
    await aprint(">   Paused for %sms!" % int(pause_time_ms))
    return [] # parameters[1:]
