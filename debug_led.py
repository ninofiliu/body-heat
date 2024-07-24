import board
import neopixel
import time
import math
import colors
import sys

nb_leds = 10
pixels = neopixel.NeoPixel(board.D18, nb_leds, auto_write=False)
for i in range(nb_leds):
    pixels[i] = (255,255,255)
pixels.show()
