from adafruit_extended_bus import ExtendedI2C as I2C
import adafruit_mlx90640
import time
import board
import busio
import adafruit_mlx90640
import math

i2c = I2C(5)
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_8_HZ
frame = [0] * 768
frame = [0] * 768
w = 32
h = 24

while True:
    try:
        mlx.getFrame(frame)
    except Exception as e:
        print("ignoring", e)
        continue
    
    if False:
        print(frame)
    if False:
        print(min(frame), max(frame))
    if True:
        t_mid = 30
        t_line = [sum([frame[w*y+x] for y in range(h)])/h for x in range(w)]
        char_line = ["X" if t > t_mid else "." for t in t_line]
        print(
            "".join(char_line),
            math.floor(min(t_line)),
            math.floor(max(t_line))
        )
