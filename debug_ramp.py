import board
import neopixel
import time
import math
import colors
import sys


def lerp(t,a,b):
	return a + t * (b-a)
	
def mix(t, aa, bb):
	return [lerp(t,a,b) for (a,b) in zip(aa,bb)]

def color_ramp(t, ramp):
	if (t<=0):
		return ramp[0]
	if (t>=1):
		return ramp[-1]
	n = len(ramp) - 1
	i = math.floor(t * n)
	u = (t * n) % 1
	return mix(u, ramp[i], ramp[i+1])

nb_leds = 187
pixels = neopixel.NeoPixel(board.D18, nb_leds, auto_write=False)
ramp = [
	(0,0,10),
	(0,10,20),
	(60,60,0),
	(255,0,0),
]
for i in range(nb_leds):
	pixels[i] = color_ramp(i/nb_leds, ramp)
pixels.show()
