import board
import neopixel
import time

nb_leds = 363

pixels = neopixel.NeoPixel(board.D18, nb_leds, auto_write=False)

while True:
	for i in range(10):
		for j in range(nb_leds):
			pixels[j] = (255/10*i,255/10*i,255/10*i);
		pixels.show()
