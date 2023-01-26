from argparse import ArgumentParser, ArgumentTypeError
from datetime import timedelta
from .LED_data.color_constants import color_from_name

### "Types" used to cleanly get data from argparse.
def time(delta: str) -> timedelta:
    """Create a timedelta object from a numerical string argument"""
    try:
        numerical_delta = float(delta)
    except ValueError:
        error = "%r is not a valid time! Expected time interval in milliseconds" % delta
        raise ArgumentTypeError(error)
    return timedelta(milliseconds=numerical_delta)

### Parameters that can easily be "subclassed" into commands.
color_parameter = ArgumentParser(add_help=False)
color_parameter.add_argument(
    "-c", "--color",
    help="Set the color of this animation",
)

future_parameter = ArgumentParser(add_help=False)
future_parameter.add_argument(
    "-n", "--next",
    nargs="+",
    help="Store a future command that we execute immediately after we complete this animation"
)

kill_parameter = ArgumentParser(add_help=False)
kill_parameter.add_argument(
    "-k", "--kill-next",
    action="store_true",
    help="Whether we should kill the animation after this dramtic interrupt!"
)

pausing_parameter = ArgumentParser(add_help=False)
pausing_parameter.add_argument(
    "-p", "--pause",
    action="store_true",
    help="Whether we should pause this animation"
)

recursion_parameter = ArgumentParser(add_help=False)
recursion_parameter.add_argument(
    "-e", "--recursive",
    action="store_true",
    help="Whether the interrupt should repeat if enter is pressed with an empty input"
)

transition_parameter = ArgumentParser(add_help=False)
transition_parameter.add_argument(
    "-t", "--transition",
    type=time,
    help="Set the amount of time it takes for this animation to complete"
)

### Convenience parameters that can be used
frame_interval_parameter = ArgumentParser(add_help=False)
frame_interval_parameter.add_argument(
    "interval",
    type=time,
    default="500",
    metavar="interval_ms",
    help="The amount of time between frames",
)


### Parsers.
alternating_parser = ArgumentParser(
    prog="alt",
    parents=[frame_interval_parameter, color_parameter, transition_parameter], 
    add_help=True
)
alternating_parser.add_argument(
    "width",
    type=int,
    default="3",
    help="The distance between pixels in the animation"
)

color_parser = ArgumentParser(
    prog="color", 
    parents=[transition_parameter],
    description="Set the color used in the animation"
)
color_parser.add_argument(
    "color", 
    type=color_from_name,
    help="The color to change the animation to"
)
color_parser.add_argument(
    "-f", "--flash",
    action="store_true",
    help="Modify the color used for the flash instead",
)

echo_parser = ArgumentParser(
    prog="echo",
    #parents=None
    add_help=True,
    description="Print the rest of this command to the terminal",
)
echo_parser.add_argument(
    "phrase",
    nargs="+",
    help="A string to echo",
)

# Exit has no parameters, and the existence of parameter is completely irrelevant. 

flash_parser = ArgumentParser(
    prog="flash",
    parents=[frame_interval_parameter, color_parameter],
    add_help=True,
    description="Make the lights flash for a brief interval before resuming the previous command",
)

fill_parser = ArgumentParser(
    prog="fill",
    parents=[color_parameter, transition_parameter],
    add_help=True,
    description="Make the lights all turn on to a single value",
)

kill_parser = ArgumentParser(
    prog="kill",
    parents=[color_parameter, transition_parameter],
    add_help=True,
    description="Turn all the lights off",
)

pause_parser = ArgumentParser(
    prog="pause",
    #parents=None,
    add_help=True,
    description="Halt the progression of the array's animation, either for a fixed interval or until the user manually overrides"
)
pause_parser.add_argument(
    "interval",
    type=time,
    default=timedelta(days=1),
    metavar="interval_ms",
    help="The amount of time to pause Leave blank to make effectively infinite",
)

pulse_parser = ArgumentParser(
    prog="pulse",
    parents=[frame_interval_parameter, color_parameter, transition_parameter],
    add_help=True,
    description="Make the lights pulse on and off, in a very menacing way"
)

traffic_parser = ArgumentParser(
    prog="traffic",
    parents=[frame_interval_parameter, color_parameter, transition_parameter],
    add_help=True,
    description="Create a traffic animation, emulating the lights of cars on a distant highway",
)

wave_parser = ArgumentParser(
    parents=[frame_interval_parameter, color_parameter, transition_parameter],
    add_help=True,
    description="Make the lights move in a continuous, wave-like fashion",
)
wave_parser.add_argument(
    "width",
    type=float,
    default="5",
    metavar="wavelength",
    help="the size of one wave in the animation",
)







