import time
import busio
import adafruit_mlx90640
import board
import neopixel

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

while True:
	try:
		mlx.getFrame(frame)
	except Exception as e:
		print("ignoring", e)
		continue
