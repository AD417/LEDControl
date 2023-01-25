from __future__ import annotations

from datetime import datetime, timedelta
from aio_stdout import aprint, flush
import asyncio 
from . import Program
from .commands import *
from .LED_data import *

will_interrupt: bool = False

async def do_my_command(full_command: str):
    """Execute a command providded by the user.\n
    Valid commands / basic info: \n
    `kill` / `off`: Kill the lights\n
    `fill` / `on`: Turn on all lights\n
    `flash`: INTERRUPT: Flash the lights for an interval.\n
    `alt`: Make the lights alternate, akin to a theater chase.\n
    `color`: Set the color of the lights.\n
    `pause`: INTERRUPT: pause the lights for an interval.\n
    `exit`: Immediately shut down and exit the application."""

    global will_interrupt

    Program.modifying_flash = False
    will_interrupt = False
    Program.next_animation = None

    parameters = full_command.split(" ")
    command = parameters.pop(0)

    if command in ALTERNATING: 
        parameters = await alt_command(parameters)
    elif command in COLOR:
        parameters = await color_command(parameters)
    elif command in ECHO:
        parameters = await echo_command(parameters)
    elif command in EXIT:
        parameters = await exit_command(parameters)
    elif command in FLASH:
        parameters = await flash_command(parameters)
    elif command in FILL:
        parameters = await fill_command(parameters)
    elif command in KILL:
        parameters = await kill_command(parameters)
    elif command in PAUSE:
        parameters = await pause_command(parameters)
    elif command in PULSE:
        parameters = await pulse_command(parameters)
    elif command in TRAFFIC:
        parameters = await traffic_command(parameters)
    elif command in WAVE:
        parameters = await wave_command(parameters)
    else:
        if (Program.is_interrupted or Program.is_paused) and command == "":
            await aprint(">   Interpreting <empty> command as request to end interrupt.")
            Program.is_interrupted = False
            Program.is_paused = False
            if Program.performing_next_command:
                await do_my_command(Program.next_command)
        else:
            await aprint("Invalid command: %s" % full_command)
        return

    Program.next_command = ""
    while len(parameters) > 0:
        # Color command.
        if parameters[0] == COLOR_PARAMETER:
            parameters = await color_command(parameters[1:])
        # Recursion parameter. 
        elif parameters[0] == RECURSION_PARAMETER:
            Program.recursive_command = full_command
            if Program.performing_recursion:
                await aprint("    Recursion continues. Type anything to break.")
            else:
                await aprint("    Initiating Recursion mode. Hit enter with a blank input to repeat last command.")
            Program.performing_recursion = True
            # Most parameters are, by design, only ever the last parameter.
            break
        elif parameters[0] == KILL_PARAMETER: 
            if not will_interrupt:
                await aprint(f"Error processing command args: 'next' parameter cannot be used with {command!r} command")
                break
            parameters = await kill_parameter(parameters[1:])
        elif parameters[0] == FUTURE_PARAMETER:
            if not (will_interrupt or Program.is_paused):
                await aprint(f"Error processing command args: 'next' parameter cannot be used with {command!r} command")
                break
            await next_command(parameters[1:])
            break
        elif parameters[0] == PAUSE_PARAMETER:
            parameters = await pause_command(parameters[1:])
        elif parameters[0] == TRANSITION_PARAMETER:
            if Program.modifying_flash:
                await aprint(f"Error Processing command args: 'transition' parameter cannot be used with {command!r} command")
                break
            parameters = await transition_parameter(parameters[1:])
        else: 
            await aprint("Error processing command args: '%s' is not a valid parameter." % parameters[0])
            break
    

    if Program.next_animation is not None:
        if Program.modifying_flash:
            Program.interrupt = Program.next_animation
        else:
            Program.animation = Program.next_animation

    if will_interrupt: Program.is_interrupted = True

def try_num(value: str) -> int:
    try: 
        return float(value)
    except ValueError: 
        return 0

async def alt_command(parameters: list[str]):
    """
    Set the state of the LEDs to alternate in a theater chase.\n
    Legal parameters:
    `Interval`: The amount of time between frames while alternating, in milliseconds. Default 500. Value must be at least 50.
    `Width`: The frequency of lit pixels, in terms of the number of LEDs between Lit pixels. Default 3. Value must be at least 2.
    """

    interval = timedelta(milliseconds=500)
    width = 3
    used_params = 0

    if len(parameters) > 0:
        interval = timedelta(milliseconds = try_num(parameters[0]))
        if interval >= timedelta(milliseconds=50): 
            used_params = 1
        else:
            interval = timedelta(milliseconds=500)

    if used_params == 1 and len(parameters) > 1: 
        width = int(try_num(parameters[1]))
        if width > 1: 
            used_params += 1
        else:
            width = 3

    Program.next_animation = AlternatingAnimation(
        color = Program.color, 
        frame_interval = interval, 
        width=width
    )

    await aprint(">   Theather Chase time!")
    await aprint(f"    Alternates every {int(interval.total_seconds() * 1000)}ms")
    await aprint(f"    1 in {width} LEDs is lit.")

    return parameters[used_params:]

async def color_command(parameters: list[str]):
    """
    Set the color used by the animation. \n
    Legal parameters:
    `color`: The name of the color being used. Required. Value can be a single letter.
    `[-f]`: If we should update the flash or not. 
    Note: if the keyword "custom" or "c" is supplied, a valid RGB value must also be supplied. See :func:`custom_color_command` for more information.
    Warning: Do not use `-f` with the color parameter or any other effects."""
    if len(parameters) == 0: 
        await aprint(">   ERROR: Color command must supply a parameter!")
        return parameters

    color_name = parameters[0]
    if len(color_name) == 1: 
        color_name = color_constants.unshorten_color(color_name)

    if color_name == "custom": 
        return await custom_color_command(parameters)

    success, color = color_constants.try_get_color(color_name)
    if not success: 
        await aprint(f"ERROR: {parameters[0]!r} is not a valid color!")
        return []

    has_flash_parameter = len(parameters) > 1 and parameters[1] == "-f"

    if will_interrupt or has_flash_parameter: 
        Program.modifying_flash = True
        Program.flash_color = color
        if Program.next_animation is not None:
            Program.next_animation.update_color_to(color)
        else:
            Program.next_animation = Program.interrupt.copy(color=color)
        await aprint(">   Flash color has been changed to: " + color_name)
        if will_interrupt and not has_flash_parameter: 
            return parameters[1:]
        return parameters[2:]

    Program.color = color
    if Program.next_animation is None:
        Program.next_animation = Program.animation.copy(color=color)
    else:
        Program.next_animation.update_color_to(color)
    await aprint(">   Primary color has been changed to: " + color_name)
    return parameters[1:]

async def custom_color_command(parameters: list[str]):
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

    color = RGB(r,g,b)

    has_flash_parameter = len(parameters) > 4 and parameters[4] == "-f"

    if Program.modifying_flash or has_flash_parameter:
        Program.modifying_flash = True
        Program.flash_color = color
        if Program.next_animation is not None:
            Program.next_animation = Program.next_animation.copy(color=color)
        else:
            Program.next_animation = Program.interrupt.copy(color=color)
        await aprint(f">   Flash color changed to a custom color: {color!r}")
        if not has_flash_parameter:
            return parameters[4:]
        return parameters[5:]

    Program.color = color
    Program.next_animation = Program.animation.copy(color=color)
    await aprint(f">   Primary color changed to a custom color: {color!r}")
    return parameters[4:]

async def echo_command(parameters: list[str]):
    """Print a statement to the console. Used in automated scripts to instruct the user on specifics involving cues."""
    output = " ".join(parameters)
    await aprint(output)
    return ""

async def exit_command(parameters: list[str]):
    Program.is_running = False
    async with flush:
        pass
    await aprint("Exiting now. Thank you for using LEDControl.")
    return []

async def fill_command(parameters: list[str]):
    """Fill the lights with a single color.\n
    Legal Parameters:
    `fill_time`: The amount of time it takes for the lights to fully fade in after the command is executed. Provided in milliseconds. Default 0 (instant)"""

    used_params = 0
    fill_time = timedelta()

    if len(parameters) > 0: 
        fill_time = timedelta(milliseconds = try_num(parameters[0]))
        if fill_time > timedelta():
            used_params += 1

    Program.next_animation = FillAnimation(color=Program.color)
    if used_params == 1:
        Program.next_animation = TransitionAnimation(fill_time, Program.animation, Program.next_animation)
    await aprint(">   Lights on!")
    return parameters[used_params:]

async def flash_command(parameters: list[str]):
    """INTERRUPT: Override the current state of the lights and flash a color. This color may be different from the base color used by the rest of the program.\n
    Legal Parameters:
    `flash_time`: The amount of time that the program spends in this flash state, in milliseconds. Default 500ms. Must be greater than 0."""

    global will_interrupt

    flash_time = timedelta(milliseconds=500)
    used_params = 0

    if len(parameters) > 0:
        flash_time = timedelta(milliseconds = try_num(parameters[0]))
        if flash_time > timedelta():
            used_params += 1
        else: 
            flash_time = timedelta(milliseconds=500)

    Program.next_animation = FlashAnimation(Program.flash_color, flash_time)
    Program.modifying_flash = True
    will_interrupt = True
    await aprint(">   Flashing!")
    await aprint("    For: %sms" % int(flash_time.total_seconds() * 1000))
    return parameters[used_params:]

async def kill_command(parameters: list[str]):
    """Completely disable the lights, setting all pixels to `RGB(0,0,0)` (black).\n
    Legal Parameters:
    `kill_time`: The amount of time it takes for the lights to fade to black after the command is executed. Provided in milliseconds. Default 0 (instant)."""

    used_params = 0
    kill_time = timedelta()

    if len(parameters) > 0: 
        kill_time = timedelta(milliseconds = try_num(parameters[0]))
        if kill_time > timedelta(milliseconds=50):
            used_params += 1

    kill_animation = KillAnimation()
    if used_params == 1:
        # TODO: -k is incompatible with the current setup for flashing.
        # To be fair, dramatic flair does not require animations. 
        Program.next_animation = TransitionAnimation(
            transition_time = kill_time, 
            current_animation = Program.animation, 
            future_animation = kill_animation
        )
    else:
        Program.next_animation = kill_animation

    await aprint(">   Killing the lights!")
    return parameters[used_params:]

async def kill_parameter(parameters: list[str]):
    """Set the next command to kill the lights. Useful for dramatic flashes ("gunshots") where the lights need to be killed suddenly.\n
    Legal Sub-parameters:
    `kill_time`: The amount of time it takes for the lights to fade to black after the command is executed. Provided in milliseconds. Default 0 (instant)."""
    used_params = 0
    kill_time = timedelta()

    if len(parameters) > 0:
        kill_time = timedelta(milliseconds = try_num(parameters[0]))
        if kill_time > timedelta(milliseconds=50):
            used_params += 1
    
    if used_params > 0:
        await next_command(["kill", parameters[0]])
    else:
        await next_command(["kill"])
    return parameters[used_params:]

async def next_command(parameters: list[str]):
    """Set the command that executes immediately after the pending interrupt. (Interrupts are signified by `INTERRUPT` in the documentation.\n
    Legal Parameters:
    `command`: The command to be executed. Required. This consists of the rest of the parameters in the command.\n
    Note: This command will not have any follow-up parameters."""
    Program.next_command = " ".join(parameters)
    Program.performing_next_command = True
    await aprint("    Next command set to: " + Program.next_command)
    return []

async def pause_command(parameters: list[str]):
    """INTERRUPT: Halt all execution. This halt may be either indefinite or for a set interval, based on supplied parameters.
    Legal Parameters:
    `pause_time_ms`: The amount of time to pause, in milliseconds. Default Infinity. Must be at least 50ms.\n
    Note: entering any command (or pressing the enter key) while the program is paused will immediately unpause. This is intended to aid in timing events with highly variable run time.\n
    Note: This comamnd will not have any follow-up parameters. Any subsequent parameters will be ignored."""
    pause_time = timedelta(milliseconds=0)
    used_params = 0

    if len(parameters) > 0:
        pause_time = timedelta(milliseconds = try_num(parameters[0]))
        if pause_time > timedelta(milliseconds=0):
            used_params += 1

    if pause_time <= timedelta(milliseconds=0):
        Program.time_to_unpause = datetime.max
        await aprint(">   Paused! (Press Enter to resume)")
    else: 
        Program.time_to_unpause = datetime.now() + pause_time
        await aprint("> Paused for %ims" % int(pause_time.total_seconds() * 1000))

    Program.is_paused = True
    return parameters[used_params:]

async def pulse_command(parameters: list[str]):
    """Generate a pulsing effect, where a color fades in and out cyclically. \n
    Legal Parameters:
    `pulse_interval`: The amount of time each pulse takes. Given in milliseconds. A pulse is the time it takes for the animation to go from fully off to fully on to fully off."""

    used_params = 0
    pulse_interval = timedelta(seconds=3)
    if len(parameters) > 0:
        pulse_interval = timedelta(milliseconds = try_num(parameters[0]))
        if pulse_interval > timedelta(milliseconds=100):
            used_params += 1
        else: 
            pulse_interval = timedelta(seconds=1)

    Program.next_animation = PulseAnimation(
        color = Program.color, 
        frame_interval = pulse_interval
    )

    await aprint(">   Pulsing the lights!")
    await aprint("    Pulse time: %ims" % int(pulse_interval.total_seconds() * 1000))
    return parameters[used_params:]

async def traffic_command(parameters: list[str]):
    """Generate a animation that simulates headlights on a distant road. \n
    Legal Parameters:
    `frame_interval`: the interval between frames. Given in milliseconds. Default 300ms. Must be at at least 100ms. An interval is the time taken for the lights to move one pixel.
    `traffic_density`: how much traffic is on the road. Given as a percentage from 0-100%. Default 10%. Values above 50% may ruin the effect."""

    used_params = 0
    frame_interval = timedelta(milliseconds=300)
    density = 0.1

    if len(parameters) > 0:
        frame_interval = timedelta(milliseconds = try_num(parameters[0]))
        if frame_interval >= timedelta(milliseconds=100):
            used_params += 1
        else:
            frame_interval = timedelta(milliseconds=300)
    
    if used_params == 1 and len(parameters) > 1:
        density = try_num(parameters[1]) / 100
        if 0 < density < 1: 
            used_params += 1
        else:
            density = 0.1

    Program.next_animation = TrafficAnimation(
        color = Program.color, 
        frame_interval = frame_interval, 
        road_size = 100, 
        traffic_density = density
    )

    await aprint(f">   Time for traffic!")
    await aprint(f"    Cars move at 1 pixel per {int(frame_interval.total_seconds() * 1000)}ms")
    await aprint(f"    About {density * 100}% of the road is used.")

    return parameters[used_params:]

async def transition_parameter(parameters: list[str]):
    """Set the amount of time we spend transitioning from the current animation state to the future one defined by the preceeding command.
    Legal Sub-parameters:
    `time`: The amount of time the program spends transitioning. Required. Provided in milliseconds. Must be greater than 50ms."""
    if len(parameters) == 0:
        await aprint("Error processing command args: '-t' parameter requires a time interval in milliseconds.")
        return []
    if issubclass(type(Program.next_animation), TransitionAnimation):
        await aprint("Error processing command args: cannot transition from a transition!")
        return parameters[1:]
    
    transition_time = timedelta(milliseconds=try_num(parameters[0]))
    if transition_time < timedelta(milliseconds=50):
        if transition_time == timedelta():
            await aprint("Error processing command args: value was either 0 or not a number!")
        else:
            await aprint("Warning: transition time provided was less than 50 *milli*seconds. Did you input seconds?")
        return parameters[1:]

    Program.next_animation = TransitionAnimation(
        transition_time = transition_time, 
        current_animation = Program.animation, 
        future_animation = Program.next_animation
    )

    return parameters[1:]

async def wave_command(parameters: list[str]):  
    """Generate a moving wave effect, as a continuous version of the `alt` command. \n
    Legal Parameters: 
    `frame_interval`: the time taken for the wave to move 1 pixel. Given in milliseconds. Default 200.
    `wave_length`: The size of one wave. Default 5.0. Can be a decimal. A wave is the distance from one fully unlit LED to another."""

    frame_interval = timedelta(milliseconds=200)
    wave_length = 5.0
    used_params = 0

    if len(parameters) > 0:
        frame_interval = timedelta(milliseconds = try_num(parameters[0]))
        if frame_interval >= timedelta(milliseconds=50): 
            used_params = 1
        else:
            frame_interval = timedelta(milliseconds=200)

    if used_params == 1 and len(parameters) > 1: 
        wave_length = try_num(parameters[1])
        if wave_length > 1: 
            used_params += 1
        else:
            wave_length = 3

    Program.next_animation = WaveAnimation(
        color = Program.color, 
        frame_interval = frame_interval, 
        wave_length = wave_length
    )

    await aprint(">   We're doing the wave!")
    await aprint(f"    Moves every {int(1000 * frame_interval.total_seconds())}ms")
    await aprint(f"    Wavelength: {wave_length}")

    return parameters[used_params:]
