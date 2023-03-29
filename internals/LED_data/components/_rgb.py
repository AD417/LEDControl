from __future__ import annotations

import math
import random
from dataclasses import dataclass

@dataclass
class RGB():
    """A singular RGB Pixel, storing a LED's state as a series of numbers. \n
    Parameters:
    `r`: the amount of red in the light.
    `g`: the amount of green in the light. 
    `b`: the amount of blue in the light."""
    r: int
    g: int
    b: int

    from dataclasses import replace as copy

    def brighten(self: RGB) -> RGB:
        factor = 255.0 / max(self.r, self.g, self.b)
        r = int(self.r * factor)
        g = int(self.g * factor)
        b = int(self.b * factor)
        return RGB(r, g, b)

    def interpolate(self: RGB, other: RGB, percent: float) -> RGB:
        """
        Interpolate between two colors in RGB space. Returns an RGB color. \n
        Parameters:
        `self` (the caller): The first color. This color will be returned if `percentage` is 0.
        `other`: The second color. This color will be returned if `percentage` is 1.
        `percentage`: The amount to interpolate between. Must be a decimal between 0 and 1, inclusive.
        `return`: an RGB value."""
        percent = max(min(percent, 1), 0)
        r = round(other.r * percent + self.r * (1 - percent))
        g = round(other.g * percent + self.g * (1 - percent))
        b = round(other.b * percent + self.b * (1 - percent))
        return RGB(r, g, b)

    def gamma_correct(self: RGB, exponent: float = 2.7) -> RGB:
        # TODO: I probably should make a lookup table for this.
        r = round(255 * math.pow(self.r / 255, exponent))
        g = round(255 * math.pow(self.g / 255, exponent))
        b = round(255 * math.pow(self.b / 255, exponent))
        return RGB(r,g,b)

    ##### DUNDER METHODS

    def __int__(self: RGB) -> int:
        """Convert the provided RGB color to a 24-bit color value. Conversion for the rpi_ws281x library."""
        # Yeah, yeah, it's RBG and not RGB. For some reason, B and G are swapped on my LEDs.
        return (self.r << 16) | (self.g << 8) | self.b

    def __str__(self: RGB) -> str:
        """Convert the provided RGB color to a hexadecimal representation (eg: #000000)"""
        return f"#{hex(self.r)[2:]:0>2}{hex(self.g)[2:]:0>2}{hex(self.b)[2:]:0>2}"
    

    # Class methods
    def random() -> RGB:
        """Generate a random color in RGB space."""
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        return RGB(r,g,b)

    def random_bright() -> RGB:
        """
        Return a random "fullbright" color. Equivalent to a HSV(random, 1, 1). \n
        Adapted from colorsys.py:
        https://github.com/python/cpython/blob/3.11/Lib/colorsys.py
        """
        hue = random.random()

        r = int(255 * (0.5 + 0.5 * math.cos(2 * math.pi * (hue))))
        b = int(255 * (0.5 + 0.5 * math.cos(2 * math.pi * (hue + 1/3))))
        g = int(255 * (0.5 + 0.5 * math.cos(2 * math.pi * (hue + 2/3))))
        """
        sector = int(hue * 6)
        sector_decimal = hue * 6 - sector

        v = 255
        p = 0
        q = int(v * (1 - sector_decimal))
        t = int(v * sector_decimal)

        r,g,b = 0,0,0
        if sector == 0:
            r,g,b = v, t, p
        if sector == 1:
            r,g,b = q, v, p
        if sector == 2:
            r,g,b = p, v, t
        if sector == 3:
            r,g,b = p, q, v
        if sector == 4:
            r,g,b = t, p, v
        if sector == 5:
            r,g,b = v, p, q
            """
        
        return RGB(r,g,b)

if __name__ == "__main__":
    for i in range(10):
        print(RGB.random_bright())