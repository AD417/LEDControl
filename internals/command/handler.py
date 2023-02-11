from __future__ import annotations

from datetime import datetime, timedelta
from types import SimpleNamespace
from typing import Any

from . import Alias
from .. import Program
from .commands import *
from .parser import *
from ..LED_data import *

Log = SimpleNamespace(data="")

def do_my_command(full_command: str|list[str]):
    """Execute a command provided by the user"""
    Log.data = ""
    parameters = []
    if isinstance(full_command, str):
        parameters = sanitize(full_command)
    else:
        parameters = full_command.copy()
    command = ""
    if len(parameters) != 0:
        command = parameters.pop(0)
    if command == "":
        command = "<null>"
    
    try:
        if command in ALIAS:
            alias_command(parameters)
        elif command in ALTERNATING: 
            alt_command(parameters)
        elif command in COLOR:
            color_command(parameters)
        elif command in ECHO:
            echo_command(parameters)
        elif command in EXIT:
            exit_command(parameters)
        elif command in FLASH:
            flash_command(parameters)
        elif command in FILL:
            fill_command(parameters)
        elif command in KILL:
            kill_command(parameters)
        elif command in PAUSE:
            pause_command(parameters)
        elif command in PULSE:
            pulse_command(parameters)
        elif command in STATUS:
            status_command(parameters)
        elif command in TRAFFIC:
            traffic_command(parameters)
        elif command in WAVE:
            wave_command(parameters)

        elif command == "<null>":
            Program.is_interrupted = False
            Program.is_paused = False
        else:
            raise TypeError("Invalid command: %s" % command)
        
        if Log.data != "":
            print(Log.data.strip("\n"))
        
    except (ValueError, TypeError) as e:
        message = str(e).strip("\n ")

        is_null_error = len(message.split(":")) == 3 and message.split(":")[2] == ""

        if not is_null_error:
            print(str(e).strip("\n"))

    if not Program.is_running: return

    if Program.performing_recursion:
        if Program.recursive_command == "":
            Program.recursive_command = full_command
    else:
        Program.recursive_command = ""

    existing_event_processing = Program.performing_next_command \
                             or Program.is_paused \
                             or Program.performing_recursion
    
    if existing_event_processing:
        print("... ", end="")
    else: 
        print("$ ", end="")
        


def sanitize(command: str) -> list[str]:
    """Sanitize and pre-process the command to prepare it for argparse"""
    if "#" in command:
        command, _ = command.split("#")
    command = command.strip().lower()

    if Alias.alias_exists_for(command):
        return Alias.command_for_alias(command)
    
    return command.split()

def validate(value: int|float|timedelta, lower: int, higher: int | None = None):
    """Evaluates if a value is within a given range.
    Parameters: 
    `value`: The value to check
    `lower`: The lower bound of acceptable values. Required.
    `upper`: The upper bound of acceptable values. Optional. If unspecified, allows for no upper limit. """

    if isinstance(value, timedelta): 
        value = float(value.total_seconds() * 1000)

    is_valid = True
    if value < lower:
        is_valid = False
    if higher is not None and value > higher:
        is_valid = False

    if is_valid: return
    
    error = "%r is not within range. " % value
    if higher is not None:
        error += "Value must be between %i and %i, inclusive." % (lower, higher)
    else:
        error += "Value must be at least %i." % lower
    raise ValueError(error)


def color_parameter(color: RGB | None, next_animation: Animation, is_flash: bool = False) -> Animation:
    if color:
        Log.data += "-c: Changing color to %r\n" % color
        if is_flash:
            Program.flash_color = color
        else:
            Program.color = color
        next_animation.update_color_to(color)
    return next_animation

def transition_parameter(transition_time: timedelta | None, next_animation: Animation) -> Animation:
    """Set the amount of time that it will take for the program to transition, if necessary. """
    if transition_time:
        Log.data += "-t: Transitioning over %ims\n" % (transition_time.total_seconds() * 1000)
        return TransitionAnimation(
            transition_time = transition_time,
            current_animation = Program.animation,
            future_animation = next_animation
        )
    return next_animation

def next_parameter(next_command: list[str] | None) -> None:
    """Set the next command to execute, if necessary."""
    if next_command is None: return

    Program.next_command = next_command
    Program.performing_next_command = True

def alias_command(parameters: list[str]):
    """
    Create a new alias that the program can use in place of a fully typed out command. \n
    Legal parameters:
    `Alias Name`: The name of the Alias. 
    `Command`: The command this alias executes. 
    """
    if len(parameters) == 0: 
        print(Alias.Aliases)
        return
    args = alias_parser.parse_args(parameters)
    
    if args.alias_name == "alias":
        raise ValueError("Cannot assign an alias to 'alias'! (ya dummy)")
    
    Alias.create_alias(args.alias_name, args.command)
    Alias.save_aliases()

    Log.data += "Alias successfully created!\n"
    Log.data += "Alias: %s\n" % args.alias_name
    Log.data += "Command: %s\n" % " ".join(args.command)

def alt_command(parameters: list[str]): 
    """
    Set the state of the LEDs to alternate in a theater chase.\n
    Legal parameters:
    `Interval`: The amount of time between frames while alternating, in milliseconds. Default 500. Value must be at least 50.
    `Width`: The frequency of lit pixels, in terms of the number of LEDs between Lit pixels. Default 3. Value must be at least 2.
    """
    args = alternating_parser.parse_args(parameters)
    
    validate(args.interval, 50)
    validate(args.width, 2)

    next_animation = AlternatingAnimation(
        color = Program.color,
        frame_interval = args.interval,
        width = args.width,
    )
    Log.data += "Theater Chase time!\n"
    Log.data += "LEDs move once every %ims\n" % (args.interval.total_seconds() * 1000)
    Log.data += "1 in %i LEDs are lit\n" % args.width
    
    next_animation = color_parameter(args.color, next_animation)
    next_animation = transition_parameter(args.transition, next_animation)
    
    Program.animation = next_animation

def color_command(parameters: list[str]):
    """
    Set the color used by the animation. \n
    Legal parameters:
    `color`: The name of the color being used. Required. Value can be a single letter.
    `[-f]`: If we should update the flash or not."""

    if len(parameters) == 0:
        Log.data += "Current main color:  %s\n" % color_constants.name_from_color(Program.color)
        Log.data += "Current flash color: %s" % color_constants.name_from_color(Program.flash_color)
        return
    
    args = color_parser.parse_args(parameters)  

    next_color = RGB(0,0,0)
    color_name = ""

    if args.color == "custom":
        next_color = custom_color_handler(args)
        color_name = repr(next_color)
    else:
        success, next_color = color_constants.try_get_color(args.color)
        if not success:
            raise ValueError("%r is an invalid color name or shorthand" % args.color)
        color_name = args.color

    if args.flash:
        next_animation = Program.interrupt.copy()
        Program.flash_color = next_color
        Log.data += "Updating the flash color to: %s\n" % color_name
    else:
        next_animation = Program.animation.copy()
        Program.color = next_color
        Log.data += "Updating the primary color to: %s\n" % color_name
    
    next_animation.update_color_to(next_color)
    
    if not args.flash:
        next_animation = transition_parameter(args.transition, next_animation)

    if args.flash:
        Program.interrupt = next_animation
    else:
        Program.animation = next_animation

def custom_color_handler(color_code: Any) -> RGB:
    valid_colors = 0
    try:
        if color_code.red != -1:
            valid_colors += 1
        if color_code.blue != -1:
            valid_colors += 1
        if color_code.green != -1:
            valid_colors += 1
        if valid_colors != 3: raise ValueError()
    except (AttributeError, ValueError):
        raise ValueError("Missing parameters: expected 3 color values but got %i" % valid_colors)
    validate(color_code.red, 0, 255)
    validate(color_code.green, 0, 255)
    validate(color_code.blue, 0, 255)
    return RGB(color_code.red, color_code.green, color_code.blue)

def echo_command(parameters: list[str]):
    """Print a statement to the console. Used in automated scripts to instruct the user on specifics involving cues."""
    print(" ".join(parameters))

def exit_command(parameters: list[str]):
    """End execution of the program. Primary way to shutdown the main event loop."""
    Program.is_running = False

def fill_command(parameters: list[str]):
    """Fill the lights with a single color."""
    args = fill_parser.parse_args(parameters)
    
    next_animation = FillAnimation(
        color = Program.color,
    )

    Log.data += "Lights on!\n"
    
    next_animation = color_parameter(args.color, next_animation)
    next_animation = transition_parameter(args.transition, next_animation)

    Program.animation = next_animation
    
def flash_command(parameters: list[str]):
    """INTERRUPT: Override the current state of the lights and flash a color. This color may be different from the base color used by the rest of the program.\n
    Legal Parameters:
    `flash_time`: The amount of time that the program spends in this flash state, in milliseconds. Default 500ms. Must be greater than 0."""
    args = flash_parser.parse_args(parameters)
    
    next_animation = FlashAnimation(
        color = Program.flash_color,
        frame_interval = args.interval
    )
    
    Log.data += "Flashing the lights!\n"
    Log.data += "Flash time: %ims\n" % (args.interval.total_seconds() * 1000)

    next_animation = color_parameter(args.color, next_animation, is_flash=True)

    if args.recursive:
        Program.performing_recursion = True

    if args.kill: next_parameter(["kill"])
    else: next_parameter(args.next)
    # print(args.next)

    Program.interrupt = next_animation
    Program.is_interrupted = True

def kill_command(parameters: list[str]):
    """Completely disable the lights, setting all pixels to `RGB(0,0,0)` (black).\n
    Legal Parameters:
    `kill_time`: The amount of time it takes for the lights to fade to black after the command is executed. Provided in milliseconds. Default 0 (instant)."""
    args = kill_parser.parse_args(parameters)

    next_animation = KillAnimation()

    Log.data += "Killing the lights!\n"
    
    next_animation = transition_parameter(args.transition, next_animation)

    Program.animation = next_animation

def pause_command(parameters: list[str]):
    """INTERRUPT: Halt all execution. This halt may be either indefinite or for a set interval, based on supplied parameters.
    Legal Parameters:
    `pause_time_ms`: The amount of time to pause, in milliseconds. Default "Infinity" (1 day).\n
    Note: entering any command (or pressing the enter key) while the program is paused will immediately unpause. This is intended to aid in timing events with highly variable run time.\n
    Note: This comamnd will not have any follow-up parameters. Any subsequent parameters will be ignored."""
    args = pause_parser.parse_args(parameters)

    Log.data += "Pausing all animations\n"
    if args.interval == timedelta(days=1):
        Log.data += "[Press enter to unpause.]\n"
    else:
        Log.data += "Pause time: %ims\n" % (args.interval.total_seconds() * 1000)

    Program.time_to_unpause = datetime.now() + args.interval
    Program.is_paused = True

def pulse_command(parameters: list[str]):
    """Generate a pulsing effect, where a color fades in and out cyclically. \n
    Legal Parameters:
    `pulse_interval`: The amount of time each pulse takes. Given in milliseconds. A pulse is the time it takes for the animation to go from fully off to fully on to fully off."""
    args = pulse_parser.parse_args(parameters)

    validate(args.interval, 500)

    next_animation = PulseAnimation(
        color = Program.color,
        frame_interval = args.interval,
    )

    Log.data += "Lights are pulsing. (Hope it's not epilleptic!)\n"
    Log.data += "Pulse interval: %ims\n" % (args.interval.total_seconds() * 1000)
    
    next_animation = color_parameter(args.color, next_animation)
    next_animation = transition_parameter(args.transition, next_animation)

    Program.animation = next_animation
    
def status_command(parameters: list[str]):
    """Display the status of the program.\n
    Legal Parameters: 
    None"""
    Log.data += "The current animation is "
    Log.data += str(Program.animation)
    color_command([])

def traffic_command(parameters: list[str]):
    """Generate a animation that simulates headlights on a distant road. \n
    Legal Parameters:
    `frame_interval`: the interval between frames. Given in milliseconds. Default 300ms. Must be at at least 100ms. An interval is the time taken for the lights to move one pixel.
    `traffic_density`: how much traffic is on the road. Given as a percentage from 0-100%. Default 10%. Values above 50% may ruin the effect."""
    args = traffic_parser.parse_args(parameters)

    validate(args.interval, 100)
    validate(args.density, 0, 100)

    next_animation = TrafficAnimation(
        color = Program.color,
        frame_interval = args.interval,
        road_size = 100,
        traffic_density = args.density * 0.01
    )

    Log.data += "Traffic time! I love the bridge.\n"
    Log.data += "Cars move 1 pixel every %ims\n" % (args.interval.total_seconds() * 1000)
    Log.data += "About %.2f%% of the road has cars on it\n" % args.density
    
    next_animation = color_parameter(args.color, next_animation)
    next_animation = transition_parameter(args.transition, next_animation)

    Program.animation = next_animation

def wave_command(parameters: list[str]):
    """Generate a moving wave effect, as a continuous version of the `alt` command. \n
    Legal Parameters: 
    `frame_interval`: the time taken for the wave to move 1 pixel. Given in milliseconds. Default 200.
    `wave_length`: The size of one wave. Default 5.0. Can be a decimal. A wave is the distance from one fully unlit LED to another."""
    args = wave_parser.parse_args(parameters)

    validate(args.interval, 100)
    validate(args.width, 2)

    next_animation = WaveAnimation(
        color = Program.color,
        frame_interval = args.interval,
        wave_length = args.width
    )

    Log.data += "We're doing the wave! \\(0-0)/\n"
    Log.data += "Animation moves 1px every %ims\n" % (args.interval.total_seconds() * 1000)
    Log.data += "The wave is %.2fpx long\n" % args.width 
    
    next_animation = color_parameter(args.color, next_animation)
    next_animation = transition_parameter(args.transition, next_animation)
    
    Program.animation = next_animation