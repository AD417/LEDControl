from __future__ import annotations
import math
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

    def interpolate(self: RGB, other: RGB, percent: float) -> RGB:
        """
        Interpolate between two colors in RGB space. Returns an RGB color. \n
        Parameters:
        `self` (the caller): The first color. This color will be returned if `percentage` is 0.
        `other`: The second color. This color will be returned if `percentage` is 1.
        `percentage`: The amount to interpolate between. Must be a decimal between 0 and 1, inclusive."""
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
        return (self.r << 16) | (self.b << 8) | self.g

    def __str__(self: RGB) -> str:
        """Convert the provided RGB color to a hexadecimal representation (eg: #000000)"""
        return f"#{hex(self.r)[2:]:0>2}{hex(self.g)[2:]:0>2}{hex(self.b)[2:]:0>2}"


if __name__ == "__main__":
    a = RGB(255,255,255)
    print(int(a))
    print(str(a))