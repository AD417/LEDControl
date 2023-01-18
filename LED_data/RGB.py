from __future__ import annotations

class RGB():
    """A singular RGB Pixel, storing a LED's state as a series of numbers. \n
    Parameters:
    `r`: the amount of red in the light.
    `g`: the amount of green in the light. 
    `b`: the amount of blue in the light."""
    def __init__(self: RGB, r: int, g: int, b: int) -> RGB:
        self.r: int = r
        self.g: int = g
        self.b: int = b

    def interpolate(self: RGB, other: RGB, percent: float) -> RGB:
        """
        Interpolate between two colors in RGB space. Returns an RGB color. \n
        Parameters:
        `self` (the caller): The first color. This color will be returned if `percentage` is 1. 
        `other`: The second color. This color will be returned if `percentage` is 1.
        `percentage`: The amount to interpolate between. Must be a decimal between 0 and 1, inclusive."""
        percent = max(min(percent, 1), 0)
        r = round(self.r * percent + other.r * (1 - percent))
        g = round(self.g * percent + other.g * (1 - percent))
        b = round(self.b * percent + other.b * (1 - percent))
        return RGB(r, g, b)

    ##### DUNDER METHODS!

    def __int__(self: RGB) -> int:
        """Convert the provided RGB color to a 24-bit color value. Conversion for the rpi_ws281x library."""
        return (self.r << 16) | (self.g << 8) | self.b
    
    def __repr__(self: RGB) -> str:
        """Convert the provided RGB color to a human-readable representation."""
        return f"RGB({self.r},{self.g},{self.b})"

    def __str__(self: RGB) -> str:
        """Convert the provided RGB color to a hexadecimal representation (eg: #000000)"""
        return f"#{hex(self.r)[2:]:0>2}{hex(self.g)[2:]:0>2}{hex(self.b)[2:]:0>2}"


    ##### CONSTANTS

    colors = {
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


if __name__ == "__main__":
    a = RGB(255,255,255)
    print(int(a))
    print(str(a))