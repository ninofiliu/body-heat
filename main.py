import adafruit_extended_bus
import adafruit_mlx90640
import board
import busio
import colors
import math
import neopixel
import time
import sys

debug = True
t_cold = 24
t_hot = 28
ramp = [
	[0,0,5],
	[0,5,20],
	[0,20,50],
	[255,0,0]
]

def mix(t, a, b):
	return [a + t * (b-a) for (a,b) in zip(a,b)]

def color_ramp(t, ramp):
	if (t<=0):
		return ramp[0]
	if (t>=1):
		return ramp[-1]
	n = len(ramp) - 1
	i = math.floor(t * n)
	u = (t * n) % 1
	return mix(u, ramp[i], ramp[i+1])

nb_leds = 720
pixels = neopixel.NeoPixel(board.D18, nb_leds, auto_write=False)

i2c = adafruit_extended_bus.ExtendedI2C(3)
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_8_HZ
frame = [0] * 768
frame = [0] * 768
w = 32
h = 24

while True:
	try:

		mlx.getFrame(frame)

		t_line = [sum([frame[w*y+x] for y in range(h)])/h for x in range(w)]
		t_min = min(t_line)
		t_max = max(t_line)
		# t_norms = [(t - t_min) / (t_max + 0.001 - t_min) for t in t_line]
		t_norms = [(t - t_cold) / (t_hot + 0.001 - t_cold) for t in t_line]
		
		if debug:
			char_line = ["X" if t > (t_min+t_max)/2 else "." for t in t_line]
			print(
				"".join(char_line),
				math.floor(min(t_line)),
				math.floor(max(t_line))
			)
		 
		for i in range(nb_leds):
			ti = (w * i) // nb_leds
			t = t_norms[ti]
			pixels[i] = color_ramp(t, ramp)
		pixels.show()
			
	except Exception as e:
		print("ignoring", e)
		continue
