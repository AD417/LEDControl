from __future__ import annotations

from datetime import datetime, timedelta
from aio_stdout import aprint, flush
import asyncio 
from . import Program
from .commands import *
from .command_parser import *
from .LED_data import *

async def do_my_command(full_command: str|list[str]):
    """Execute a command provided by the user"""
    parameters = sanitize(full_command)
    if len(parameters) != 0:
        command = parameters.pop(0)
    else:
        command = ""

    if command in ALTERNATING: 
        parameters = alt_command(parameters)
    elif command in COLOR:
        parameters = color_command(parameters)
    elif command in ECHO:
        parameters = echo_command(parameters)
    elif command in EXIT:
        parameters = exit_command(parameters)
    elif command in FLASH:
        parameters = flash_command(parameters)
    elif command in FILL:
        parameters = fill_command(parameters)
    elif command in KILL:
        parameters = kill_command(parameters)
    elif command in PAUSE:
        parameters = pause_command(parameters)
    elif command in PULSE:
        parameters = pulse_command(parameters)
    elif command in TRAFFIC:
        parameters = traffic_command(parameters)
    elif command in WAVE:
        parameters = wave_command(parameters)
        
    elif (Program.is_interrupted or Program.is_paused) and command == "":
        Program.is_interrupted = False
        Program.is_paused = False
    else:
        await aprint("Invalid command: %s" % full_command)


def sanitize(command: str) -> list[str]:
    """Sanitize and pre-process the command to prepare it for argparse"""
    if "#" in command:
        command, _ = command.split("#")
    command = command.strip().lower()

    next_command = ""
    if "-n" in command:
        splitter = "-n"
        using_next_over_n = "--next" in command and command.index("--next") < command.index("-n")
        if using_next_over_n:
            splitter = "--next"
        command, next_command = command.split(splitter, 1)

    command = command.strip().lower()
    next_command = next_command.strip().lower()

    parameters = command.split()
    if next_command == "":
        return parameters
    return command.split() + [splitter, next_command]

def alt_command(parameters: list[str]): 
    try:
        args = alternating_parser.parse_args(parameters)
    except SystemExit:
        return 
    
    next_animation = AlternatingAnimation(
        color = Program.color,
        frame_interval = args.interval,
        width = args.width,
    )
    if args.color:
        Program.color = args.color
        next_animation.update_color_to(args.color)
    
    if args.transition:
        next_animation = TransitionAnimation(
            transition_time = args.transition,
            current_animation = Program.animation,
            future_animation = next_animation
        )
    
    Program.animation = next_animation

def color_command(parameters: list[str]):
    try:
        args = color_parser.parse_args(parameters)
    except SystemExit:
        return

    if args.flash:
        next_animation = Program.interrupt.copy()
        Program.flash_color = args.color
    else:
        next_animation = Program.animation.copy()
        Program.color = args.color
    
    next_animation.update_color_to(args.color)
    
    if not args.flash and args.transition:
        next_animation = TransitionAnimation(
            transition_time = args.transition,
            current_animation = Program.animation,
            future_animation = next_animation
        )

    if args.flash:
        Program.interrupt = next_animation
    else:
        Program.animation = next_animation

def echo_command(parameters: list[str]):
    print(" ".join(parameters))

def exit_command(parameters: list[str]):
    Program.is_running = False

def flash_command(parameters: list[str]):
    try:
        args = flash_parser.parse_args(parameters)
    except SystemExit:
        return
    
    next_animation = FlashAnimation(
        color = Program.color,
        frame_interval = args.interval
    )

    if args.color:
        Program.flash_color = args.color
        next_animation.update_color_to(args.color)

    Program.interrupt = next_animation
    Program.is_interrupted = True

def fill_command(parameters: list[str]):
    try:
        args = fill_parser.parse_args(parameters)
    except SystemExit:
        return
    
    next_animation = FillAnimation(
        color = Program.color,
    )
    if args.color:
        next_animation.update_color_to(args.color)
    if args.transition:
        next_animation = TransitionAnimation(
            transition_time = args.transition,
            current_animation = Program.animation,
            future_animation = next_animation
        )
    Program.animation = next_animation
    
def kill_command(parameters: list[str]):
    try:
        args = kill_parser.parse_args(parameters)
    except SystemExit:
        return
    next_animation = KillAnimation()

    if args.transition:
        next_animation = TransitionAnimation(
            transition_time = args.transition,
            current_animation = Program.animation,
            future_animation = next_animation
        )
    Program.animation = next_animation

def pause_command(parameters: list[str]):
    try:
        args = pause_parser.parse_args(parameters)
    except SystemExit:
        return
    Program.time_to_unpause = datetime.now() + args.interval
    Program.is_paused = True

def pulse_command(parameters: list[str]):
    try:
        args = pulse_parser.parse_args(parameters)
    except SystemExit:
        return
    next_animation = PulseAnimation(
        color = Program.color,
        frame_interval = args.interval,
    )
    if args.color:
        Program.color = args.color
        next_animation.update_color_to(args.color)
    
    if args.transition:
        next_animation = TransitionAnimation(
            transition_time = args.transition_time,
            current_animation = Program.animation,
            future_animation = next_animation
        )
    Program.animation = next_animation
    
def traffic_command(parameters: list[str]):
    try:
        args = traffic_parser.parse_args(parameters)
    except SystemExit:
        return
    next_animation = TrafficAnimation(
        color = Program.color,
        frame_interval = args.interval,
        road_size = 100,
        traffic_density = args.density * 0.01
    )

    if args.color:
        Program.color = args.color
        next_animation.update_color_to(args.color)
    if args.transition:
        next_animation = TransitionAnimation(
            transition_time = args.transition,
            current_animation = Program.animation,
            future_animation = next_animation
        )
    Program.animation = next_animation

def wave_command(parameters: list[str]):
    try:
        args = wave_parser.parse_args(parameters)
    except SystemExit:
        return
    next_animation = WaveAnimation(
        color = Program.color,
        frame_interval = args.interval,
        wave_length = args.width
    )

    if args.color:
        Program.color = args.color
        next_animation.update_color_to(args.color)
    if args.transition:
        next_animation = TransitionAnimation(
            transition_time = args.transition,
            current_animation = Program.animation,
            future_animation = next_animation,
        )
    Program.animation = next_animation