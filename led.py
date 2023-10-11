import board
import neopixel
import time
import math

nb_leds = 720
pixels = neopixel.NeoPixel(board.D18, nb_leds, auto_write=False)

cold = [0,0,50]
mid = [50,15,0]
hot = [255,5,0]

def mix(t, a, b):
	print(t, a, b)
	return [a + t * (b-a) for (a,b) in zip(a,b)]

def color_ramp(t, ramp):
	if (t==1):
		return ramp[-1]
	n = len(ramp) - 1
	i = math.floor(t * n)
	u = (t * n) % 1
	return mix(u, ramp[i], ramp[i+1])

print(color_ramp(0.75, [cold, mid, hot]))

"""
for i in range(nb_leds):
	t = None
	a = None
	b = None
	if i < nb_leds / 2:
		t = i / (nb_leds / 2)
		a = cold
		b = mid
	else:
		t = (i - (nb_leds / 2)) / (nb_leds / 2)
		a = cold
		b = mid
	pixels[i] = interpolate(a, b)
pixels.show()
"""
