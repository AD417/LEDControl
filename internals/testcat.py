import time
import board
import neopixel

PIXELS = 100
ALT_SIZE = 3

# Initialize the Neopixel strip on pin 21 with 8 pixels
strip = neopixel.NeoPixel(board.D21, PIXELS)

for i in range(10):
    for j in range(PIXELS):
        if (i + j) % ALT_SIZE == 0: strip[j] = (255, 255, 255)
        else: strip[j] = (0, 0, 0)

    strip.show()
    time.sleep(0.5)

for i in range(PIXELS):
    strip[i] = (0,0,0)

print("DONE!")