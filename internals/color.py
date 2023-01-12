COLORS = {
    "red": 0xFF0000,
    "orange": 0xFF3F00,
    "yellow": 0xFFFF00,
    "green": 0x008000,
    "blue": 0x0000FF,
    "magenta": 0xFF00FF,
    "purple": 0x9400D3,
    # Actually purple, but imabalnces cause some interesting behaviour. 
    "pink": 0xFF60FF,
    "white": 0xFFFFFF,
    "black": 0x000000,
}

def try_get_color(name: str):
    color = 0x000000
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


if __name__ == "__main__":
    success, color = try_get_color("pink")
    print(color)