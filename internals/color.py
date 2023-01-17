COLORS = {
    "black": 0x000000,
    "blue": 0x0000FF,
    "green": 0x008000,
    "magenta": 0xFF00FF,
    "orange": 0xFF3F00,
    # Actually purple, but color imabalnces cause some interesting behaviour. 
    "pink": 0xFF60FF,
    "purple": 0x9400D3,
    "red": 0xFF0000,
    "white": 0xFFFFFF,
    "yellow": 0xFF8F00,

    
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
    color = 0x000000
    if len(name) == 1: 
        try:
            name = COLOR_SHORTHAND[name]
        except KeyError:
            return False, (0,0,0)
    # Check to make sure the color specified actually exists. 
    try: 
        color = COLORS[name]
    except KeyError:
        return False, (0,0,0)
    
    # 255 * 256^2 = 16,711,680
    r = (color & 16711680) >> 16
    # Due to reasons, these two need to be swapped. Probably only on this implementation. 
    # 255 * 256 = 65280
    b = (color & 65280) >> 8
    # 255 masks all the bits in one of the colors.
    g = color & 255

    return True, (r,g,b)

def unshorten_color(char: str):
    try:
        return COLOR_SHORTHAND[char]
    except KeyError:
        return ""

if __name__ == "__main__":
    success, color = try_get_color("pink")
    print(color)