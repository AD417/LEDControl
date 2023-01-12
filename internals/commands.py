from rpi_ws281x import PixelStrip, Color
import time

def set_color(Program, r, g, b) -> bool:
    try: 
        data = (int(r), int(g), int(b))
        Program.color = data
        return True
    except ValueError: 
        return False

def fill(strip, color):
    """Instataneously set the entire array to some color."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()

# Define functions which animate LEDs in various ways.
def colorWipe(strip: PixelStrip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChase(strip: PixelStrip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

def theaterChaseFrame(strip, color, Program):
    """Movie theater light style chaser animation."""
    for i in range(0, strip.numPixels(), Program.max_animation):
        strip.setPixelColor(i + Program.animation, color)
    strip.show()
    for i in range(0, strip.numPixels(), Program.max_animation):
        strip.setPixelColor(i + Program.animation, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

'''
def rainbow(strip: PixelStrip, wait_ms: int=20, iterations: int=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def rainbowCycle(strip: PixelStrip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel(
                (int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChaseRainbow(strip: PixelStrip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

'''