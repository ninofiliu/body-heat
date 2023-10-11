import board
import neopixel
import time
import math
import colors

nb_leds = 720
pixels = neopixel.NeoPixel(board.D18, nb_leds, auto_write=False)

cold = [0,0,50]
mid = [50,15,0]
hot = [255,5,0]

for i in range(nb_leds):
	pixels[i] = colors.color_ramp(i/nb_leds, [
		[0,0,50],
		[50,15,0],
		[255,5,0],
	])
