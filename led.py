import board
import neopixel
import time

nb_leds = 720

pixels = neopixel.NeoPixel(board.D18, nb_leds, auto_write=False)

cold = [0,0,50]
mid = [50,15,0]
hot = [255,5,0]

# interpolate colors
def interpolate(a, b):
	return [a + t * (b-a) for (a,b) in zip(cold, mid)]

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
