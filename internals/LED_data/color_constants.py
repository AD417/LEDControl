from __future__ import annotations

import argparse

from .RGB import RGB

COLORS = {
    "black": RGB(0, 0, 0),
    "blue": RGB(0, 0, 255),
    "daytime": RGB(255, 127, 63),
    "green": RGB(0, 255, 0),
    "magenta": RGB(255, 0, 255),
    "midnight": RGB(63, 0, 127),
    "orange": RGB(255, 127, 0),
    # Actually purple, but color imabalnces cause some interesting behaviour. 
    "pink": RGB(255, 100, 255),
    "purple": RGB(200, 0, 255),
    "red": RGB(255, 0, 0),
    "white": RGB(255, 255, 255),
    "yellow": RGB(255, 191, 0),
}

COLOR_SHORTHAND = {
    "b": "blue",
    # Potential collision with "cyan".
    "c": "custom",
    "d": "daytime",
    "g": "green",
    # Avoids a collision with magenta.
    "i": "midnight",
    # Avoids a collision with blue.
    "k": "black",
    # Avoids a collosion with pink. 
    "m": "purple",
    "o": "orange",
    "p": "pink",
    "r": "red",
    "w": "white",
    "y": "yellow",
}

def color_from_name(name: str):
    """Get a full color name from a single-letter shorthand. \n
    Parameters:
    `name`: A letter for the color we are extracting.
    `returns`: a longer name indicating the full name of the color.
    `raises`: `ValueError`, if the shorthand is invalid."""
    try:
        if len(name) == 1:
            name = COLOR_SHORTHAND[name]
        return COLORS[name]
    except KeyError:
        error = "%r is not a valid color name or shorthand" % name
        raise ValueError(error)

def try_get_color(name: str):
    """Create an RGB color from a name.
    Parameters:
    `name`: the name of the color used. Cannot be a shorthand.
    `returns`: a boolean indicating if the operation was successful, and an RGB color."""
    name = name.lower()
    color = None
    # Check to make sure the color specified actually exists. 
    try: 
        color = COLORS[name]
    except KeyError:
        return False, RGB(0,0,0)

    return True, color

def unshorten_color(char: str):
    try:
        return COLOR_SHORTHAND[char]
    except KeyError:
        return ""