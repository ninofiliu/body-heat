import time
import board
import busio
import adafruit_mlx90640

i2c = busio.I2C(board.SCL, board.SDA)
mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C", [hex(i) for i in mlx.serial_number])
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ

frame = [0] * 768
while True:
	try:
		mlx.getFrame(frame)
	except Exception as e:
		print("Ignoring", e)
		continue
	print(min(frame), max(frame))
