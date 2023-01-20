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
        r = round(other.r * percent + self.r * (1 - percent))
        g = round(other.g * percent + self.g * (1 - percent))
        b = round(other.b * percent + self.b * (1 - percent))
        return RGB(r, g, b)

    ##### DUNDER METHODS

    def __int__(self: RGB) -> int:
        """Convert the provided RGB color to a 24-bit color value. Conversion for the rpi_ws281x library."""
        return (self.r << 16) | (self.b << 8) | self.g
    
    def __repr__(self: RGB) -> str:
        """Convert the provided RGB color to a human-readable representation."""
        return f"RGB({self.r},{self.g},{self.b})"

    def __str__(self: RGB) -> str:
        """Convert the provided RGB color to a hexadecimal representation (eg: #000000)"""
        return f"#{hex(self.r)[2:]:0>2}{hex(self.g)[2:]:0>2}{hex(self.b)[2:]:0>2}"


if __name__ == "__main__":
    a = RGB(255,255,255)
    print(int(a))
    print(str(a))