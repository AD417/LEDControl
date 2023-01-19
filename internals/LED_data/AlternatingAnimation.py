from __future__ import annotations
from .Animation import Animation
from .RGB import RGB
from typing import Any

class AlternatingAnimation(Animation):
    def __init__(self: Animation, color: RGB, frame_interval_sec: float = 0, width: int = 3):
        super().__init__(color, frame_interval_sec)
        self.width = width

    kill_color = RGB(0,0,0)
    def pixel_state(self: AlternatingAnimation, pixel_id: int) -> RGB:
        frame = self.frame()
        if (frame + pixel_id) % self.width == 0: return self.color
        return self.kill_color

if __name__ == "__main__":
    from rpi_ws281x import PixelStrip
    from RGBArray import RGBArray

    # LED strip configuration:
    LED_COUNT = 100        # Number of LED pixels.
    LED_PIN = 18          # GPIO pin connected to the pixels (18 uses PWM!).
    # LED_PIN = 10        # GPIO pin connected to the pixels (10 uses SPI /dev/spidev0.0).
    LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA = 10          # DMA channel to use for generating signal (try 10)
    LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
    LED_INVERT = False    # True to invert the signal (when using NPN transistor level shift)
    LED_CHANNEL = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53

    STRIP = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
    STRIP.begin()

    array = RGBArray(100)
    anim = AlternatingAnimation(RGB(255, 0, 0), frame_interval_sec=0.1, width=10)
    while anim.frame() < 100:
        array.update_strip_using(anim)
        array.send_output_to(STRIP)