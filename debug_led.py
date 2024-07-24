import board
import neopixel
import time
import math
import colors
import sys

nb_leds = int(sys.argv[1]) # 187
pixels = neopixel.NeoPixel(board.D18, nb_leds, auto_write=False)
while True:
	for i in range(nb_leds):
	    pixels[i] = (10,0,0)
	pixels.show()
	time.sleep(1/24)
	for i in range(nb_leds):
	    pixels[i] = (0,10,0)
	pixels.show()
	time.sleep(1/24)
