from __future__ import annotations

from rpi_ws281x import PixelStrip

# from ._Animation.Animation import Animation
from .RGB import RGB

class RGBArray():
    def __init__(self: RGBArray, array_length: int):
        assert array_length > 0

        self._array: list[RGB] = []
        self.size = array_length

        for _ in range(array_length): 
            self._array.append(RGB(0,0,0))

    # def update_strip_using(self: RGBArray, animation: Animation):
    #     for pixel in range(self.size):
    #         self._array[pixel] = animation.pixel_state(pixel)

    def send_output_to(self: RGBArray, strip: PixelStrip, update: bool = True):
        """Send the data from the RGB Array to the pixel_id strip output. \n
        Parameters: 
        `strip`: The rpi_ws281x PixelStrip we are putting the data in.
        `update`: Whether the PixelStrip should immediately update after this operation."""
        assert self.size >= strip.numPixels()
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, int(self._array[i].gamma_correct()))
        if update: strip.show()

    def blank_copy(self: RGBArray):
        return RGBArray(self.size)
        
    def interpolate(self: RGBArray, other: RGBArray, percentage: float):
        """
        Interpolate every LED in a strip between two colors in RGB space. Returns an RGB color. \n
        Parameters:
        `self` (the caller): The first strip. This strip will be returned if `percentage` is 0.
        `other`: The second strip. This strip will be returned if `percentage` is 1. This strip must have the same length as the `self`. 
        `percentage`: The amount to interpolate between. Must be a decimal between 0 and 1, inclusive.
        `return`: an RGBArray."""
        assert self.size == other.size
        output = self.blank_copy()
        for pixel in range(self.size):
            output._array[pixel] = self._array[pixel].interpolate(other._array[pixel], percentage)
        return output

    def __repr__(self: RGBArray) -> str:
        return f"RGBArray({self.size}"

    def __getitem__(self: RGBArray, key: int):
        if not isinstance(key, int): raise TypeError("Invalid index: %r" % key)
        return self._array[key]

    def __setitem__(self: RGBArray, key: int, item: RGB):
        if not isinstance(key, int): raise TypeError("Invalid index: %r" % key)
        if not isinstance(item, RGB): raise TypeError("Invalid color: %r" % key)
        self._array[key] = item

if __name__ == "__main__":
    import time
    # LED strip configuration:
    LED_COUNT = 20        # Number of LED pixels.
    LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
    # LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10          # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    strip.begin()
    a = RGBArray(20)
    for i in range(a.size):
        a._array[i] = RGB(255,255,255)
    a.send_output_to(strip)
    time.sleep(3)
    a = RGBArray(20)
    a.send_output_to(strip)
    