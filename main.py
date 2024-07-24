import adafruit_mlx90640
import board
import busio
import colors
import math
import neopixel
import sys
import time

# params
debug = True
t_cold = 24
t_hot = 28
ramp = [
	[0,0,5],
	[0,5,20],
	[0,20,50],
	[255,0,0]
]

# utils
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
	
# setup leds
nb_leds = 187
pixels = neopixel.NeoPixel(board.D18, nb_leds, auto_write=False)

# setup cam
i2c = busio.I2C(board.SCL, board.SDA, frequency=800000)
mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C", [hex(i) for i in mlx.serial_number])
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ
frame = [0] * 768
w = 32
h = 24
t_smooth_min = 20

# run
while True:
	try:
		mlx.getFrame(frame)

		t_line = [sum([frame[w*y+x] for y in range(h)])/h for x in range(w)]
		t_max = max(t_line)
		t_min = min(t_line)
		t_smooth_min = t_smooth_min + 0.05 * (t_min-t_smooth_min)
		t_cold = t_smooth_min
		t_hot = 34
		t_norms = [(t - t_cold) / (t_hot - t_cold) for t in t_line]
		
		if debug:
			char_line = ["X" if t > (t_min+t_max)/2 else "." for t in t_line]
			print(
				"".join(char_line),
				math.floor(t_smooth_min),
				math.floor(t_min),
				math.floor(t_max)
			)
		 
		for i in range(nb_leds):
			ti = i * w / nb_leds
			ti_floor = math.floor(ti)
			ti_fract = ti % 1
			t_down = t_norms[ti_floor]
			t_up = t_norms[min(ti_floor+1,len(t_norms)-1)]
			t = lerp(ti_fract, t_down, t_up)
			pixels[i] = color_ramp(t, ramp)
		pixels.show()
			
	except Exception as e:
		print("ignoring", e)
		continue
