import board
import neopixel
import time
import math
import colors
import sys

nb_leds = int(sys.argv[1])

pixels = neopixel.NeoPixel(board.D18, nb_leds, auto_write=False)

while True:
	for i in range(nb_leds):
		pixels[i] = (1,1,1)
	pixels.show()
	time.sleep(1)
	for i in range(nb_leds):
		pixels[i] = (2,2,2)
	pixels.show()
	time.sleep(1)
	
