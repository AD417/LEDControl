from __future__ import annotations

from aio_stdout import ainput, aprint
import asyncio
from .utils import try_num
from .color import try_get_color


async def alt_command(parameters: list[str], Program):
    Program.interrupt = False
    Program.state = 2
    interval = 500
    width = 3
    used_params = 0

    if len(parameters) > 0:
        interval = try_num(parameters[0])
    if interval >= 50: 
        Program.interval = interval * 0.001
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
    Program.interrupt = False
    Program.state = 1
    # TODO: Fadein animation data

    await aprint(">   Lights on!")
    return parameters

async def flash_command(parameters: list[str], Program):
    Program.interrupt = True
    await aprint(">   Flashing!")
    Program.interrupt_state = 1
    if len(parameters) == 0: 
        Program.interrupt_timer = 1
        await aprint("    For: 1000ms")
        return parameters
    
    flash_time = try_num(parameters[0])
    if flash_time <= 0: flash_time = 1000
    Program.interrupt_timer = flash_time * 0.001
    await aprint("    For: %sms" % int(flash_time))
    return parameters[1:]

async def kill_command(parameters: list[str], Program):
    Program.interrupt = False
    Program.state = 0
    # TODO: Fadeout animation data

    await aprint(">   Killing the lights!")
    return parameters

async def pause_command(parameters: list[str], Program):
    Program.interrupt = True
    Program.interrupt_state = 0
    # TODO: Test this code's interaction with flash. Pause on a flash could work with this, but would be super scuffed!
    if len(parameters) == 0:
        # An arbitrarily large number. 
        Program.interrupt_timer = 100000
        await aprint(">   Paused!")
        return [] # parameters
    time_ms = try_num(parameters[0])
    if time_ms < 50:
        await aprint(">   Paused! (Expected parameter 'time' not valid)")
        Program.interrupt_timer = 100000
        return parameters
    Program.interrupt_timer = time_ms * 0.001
    await aprint(">   Paused for %sms!" % int(time_ms))
    return [] # parameters[1:]
