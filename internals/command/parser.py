from __future__ import annotations

from argparse import ArgumentParser, ArgumentTypeError, ArgumentError
from datetime import timedelta
from typing import NoReturn

from ..LED_data.color_constants import color_from_name, unshorten_color

### Exit-avoiding version of argparse. 
class LEDParser(ArgumentParser):
    def exit(self, status: int = ..., message: str | None = "") -> NoReturn:
        if message is None:
            message = ""
        raise ValueError(message)


### "Types" used to cleanly get data from argparse.
def time(delta: str) -> timedelta:
    """Create a timedelta object from a numerical string argument"""
    try:
        numerical_delta = float(delta)
    except ValueError:
        error = "%r is not a valid time! Expected time interval in milliseconds" % delta
        raise ArgumentTypeError(error)
    return timedelta(milliseconds=numerical_delta)

def color_name(color: str) -> str:
    new_color = color
    if len(color) == 1:
        new_color = unshorten_color(color)
    if len(new_color) == 0:
        raise ArgumentError("Invalid color name: %r" % color)
    return new_color

### Otherwise optional parameters to add to parsers
def add_color_to(parser: LEDParser):
    parser.add_argument(
        "-c", "--color",
        type=color_from_name,
        help="Set the color of this animation",
    )

def add_future_to(parser: ArgumentParser):
    parser.add_argument(
        "-n", "--next",
        nargs="...",
        help="Store a future command that we execute immediately after we complete this animation"
    )

def add_kill_to(parser: LEDParser):
    parser.add_argument(
        "-k", "--kill",
        action="store_true",
        help="Whether we should kill the animation after this dramtic interrupt!"
    )

def add_pause_to(parser: LEDParser):
    parser.add_argument(
        "-p", "--pause",
        action="store_true",
        help="Whether we should pause this animation"
    )

def add_recursion_to(parser: LEDParser):
    parser.add_argument(
        "-e", "--recursive",
        action="store_true",
        help="Whether the interrupt should repeat if enter is pressed with an empty input"
    )

def add_transition_to(parser: LEDParser):
    parser.add_argument(
        "-t", "--transition",
        type=time,
        metavar="TIME",
        help="Set the amount of time it takes for this animation to complete"
    )


### Positional parameters that can be added
def add_required_interval_to(parser: LEDParser, default_value_ms: int = 500):
    parser.add_argument(
        "interval",
        type=time,
        nargs="?",
        default=str(default_value_ms),
        metavar="interval_ms",
        help="The amount of time between frames",
    )

def add_required_width_to(parser: LEDParser, is_int: bool = False, default_width_px: int = 3, help: str = ""):
    parser.add_argument(
        "width",
        type=int if is_int else float,
        nargs="?",
        default=str(default_width_px),
        metavar="width",
        help="The space between bright pixels on the display" if help == "" else help,
    )

### Parsers.
alias_parser = LEDParser(
    prog="alias",
    description="Create a new alias for a long command you hate typing out or need to use repeatedly",
    epilog="These aliases are stored locally. Edit the /config/alias file to edit or remove",
)
alias_parser.add_argument(
    "alias_name",
    metavar="name",
    help="The name of the alias",
)
alias_parser.add_argument(
    "command",
    nargs="...",
    help="The command that this alias executes",
)

alternating_parser = LEDParser(
    prog="alt",
    description="Set the lights to alternate in a \"Theater Chase\" Animation.")
add_required_interval_to(alternating_parser)
add_required_width_to(alternating_parser, is_int=True, help="The distance between pixels in the animation")
add_color_to(alternating_parser)
add_transition_to(alternating_parser)

color_parser = LEDParser(
    prog="color", 
    description="Set the color used in the animation"
)
color_parser.add_argument(
    "color", 
    type=color_name,
    help="The color to change the animation to"
)
color_parser.add_argument(
    "red",
    type=int,
    default=-1,
    nargs="?",
    metavar="R",
    help="An amount of red to add. Requires \"color\" to be custom."
)
color_parser.add_argument(
    "green",
    type=int,
    default=-1,
    nargs="?",
    metavar="G",
    help="An amount of green to add. Requires \"color\" to be custom."
)
color_parser.add_argument(
    "blue",
    type=int,
    default=-1,
    nargs="?",
    metavar="B",
    help="An amount of blue to add. Requires \"color\" to be custom."
)
color_parser.add_argument(
    "-f", "--flash",
    action="store_true",
    help="Modify the color used for the flash instead",
)
add_transition_to(color_parser)

# Echo needs no special parameter processing. 

# Exit has no parameters, and the existence of parameter is completely irrelevant. 

flash_parser = LEDParser(
    prog="flash",
    description="Make the lights flash for a brief interval before resuming the previous command",
)
add_required_interval_to(flash_parser)
add_color_to(flash_parser)
flash_parser_futures = flash_parser.add_mutually_exclusive_group()
add_future_to(flash_parser_futures)
add_kill_to(flash_parser_futures)

add_recursion_to(flash_parser)

fill_parser = LEDParser(
    prog="fill",
    description="Make the lights all turn on to a single value",
)
add_color_to(fill_parser)
add_transition_to(fill_parser)

kill_parser = LEDParser(
    prog="kill",
    description="Turn all the lights off",
)
add_transition_to(kill_parser)

pause_parser = LEDParser(
    prog="pause",
    description="Halt the progression of the array's animation, either for a fixed interval or until the user manually overrides"
)
pause_parser.add_argument(
    "interval",
    type=time,
    nargs="?",
    default=timedelta(days=1),
    metavar="interval-ms",
    help="The amount of time to pause. Leave blank to make effectively infinite",
)

pulse_parser = LEDParser(
    prog="pulse",
    description="Make the lights pulse on and off, in a very menacing way",
    epilog="Be careful with low values, as it may cause adverse effects for viewers with epillepsy."
)
add_required_interval_to(pulse_parser, default_value_ms=3000)
add_color_to(pulse_parser)
add_transition_to(pulse_parser)

status_parser = LEDParser(
    prog="status",
    description="Display important status information regarding the program",
    epilog="Are you debugging something? Report bugs to AD417."
)
status_parser.add_argument(
    # TODO: determine if this should be changed to a "count" argument. (eg: -aaaaa)
    "-a", "--all",
    action="store_true",
    help="Whether ALL program information should be displayed, including internal/debug variables."
)

traffic_parser = LEDParser(
    prog="traffic",
    description="Create a traffic animation, emulating the lights of cars on a distant highway",
)
add_required_interval_to(traffic_parser, default_value_ms=250)
add_color_to(traffic_parser)
add_transition_to(traffic_parser)
traffic_parser.add_argument(
    "density",
    type=float,
    nargs="?",
    default=10,
    metavar="traffic-density",
    help="The percentage of the road taken up by cars."
)

wave_parser = LEDParser(
    prog="wave",
    description="Make the lights move in a continuous, wave-like fashion",
)
add_required_interval_to(wave_parser)
add_color_to(wave_parser)
add_transition_to(wave_parser)
add_required_width_to(wave_parser, help="the size of one wave in the animation")