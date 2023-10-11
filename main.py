import time
import busio
import adafruit_mlx90640
import board
import neopixel
import math
import colors

# leds init
nb_leds = 363
pixels = neopixel.NeoPixel(board.D18, nb_leds, auto_write=False)

# cam init
i2c = busio.I2C(board.SCL, board.SDA)
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_8_HZ
frame = [0] * 768
w = 32
h = 24

# parameters
ramp = [
	[0,0,50],
	[50,15,0],
	[255,5,0],
]

while True:
	# reading cam
	try:
		mlx.getFrame(frame)
	except Exception as e:
		print("ignoring", e)
		continue
	
	# painting leds
	t_line = [sum([frame[w*y+x] for y in range(h)])/h for x in range(w)]
	t_min = min(t_line)
	t_max = min(t_line) + 0.01
	for pi in range(nb_leds):
		ti = pi*w//nb_leds
		tn = (t_line[ti] - t_min) / (t_max - t_min)
		pixels[pi] = colors.color_ramp(tn, ramp)

	# debug
	char_line = ["X" if t > t_mid else "." for t in t_line]
	print(
		"".join(char_line),
		math.floor(min(t_line)),
		math.floor(max(t_line))
	)
