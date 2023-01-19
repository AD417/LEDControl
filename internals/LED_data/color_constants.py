from __future__ import annotations

from .RGB import RGB

COLORS = {
    "black": RGB(0, 0, 0),
    "blue": RGB(0, 0, 255),
    "green": RGB(0, 128, 0),
    "magenta": RGB(255, 0, 255),
    "orange": RGB(255, 63, 0),
    # Actually purple, but color imabalnces cause some interesting behaviour. 
    "pink": RGB(255, 100, 255),
    "purple": RGB(0x94, 0, 0xD3),
    "red": RGB(255, 0, 0),
    "white": RGB(255, 255, 255),
    "yellow": RGB(255, 127, 0),
}

COLOR_SHORTHAND = {
    "b": "blue",
    # Potential collision with "cyan".
    "c": "custom", 
    "g": "green",
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

def try_get_color(name: str):
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