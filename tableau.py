import time
import board
import busio
import adafruit_mlx90640
import requests
import json


screen_w = 43
screen_h = 16
chunk_size = 256
nb_leds = 678
to_pop = [
    (0, 0),
    (42, 0),
    (20, 7),
    (21, 7),
    (22, 7),
    (20, 8),
    (21, 8),
    (22, 8),
    (0, 15),
    (42, 15),
]

cam_w = 32
cam_h = 24


# col_mat = [
#     [f"{x*256//w:02X}{y*256//h:02X}{'FF' if x==0 else '00'}" for x in range(w)]
#     for y in range(h)
# ]
# col_mat = [[f"{'FF' if x %2==0 else '00'}0000" for x in range(w)] for y in range(h)]


def paint(col_mat: list[list[str]]) -> None:
    for x, y in to_pop[::-1]:
        col_mat[y].pop(x)
    col_rev = [col_mat[i] if i % 2 == 0 else col_mat[i][::-1] for i in range(screen_h)]
    col_arr = [col for line in col_rev for col in line]
    for chunk_start in range(0, nb_leds, chunk_size):
        col_chunk = col_arr[chunk_start : chunk_start + chunk_size]
        requests.post(
            "http://4.3.2.1/json",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"bri": 255, "seg": {"i": [chunk_start] + col_chunk}}),
        )


def resize(image, w2, h2):
    w1 = len(image[0])
    h1 = len(image)
    # Create a new image with the desired dimensions
    resized_image = [[0 for _ in range(w2)] for _ in range(h2)]

    # Calculate scaling factors
    x_ratio = float(w1 - 1) / (w2 - 1) if w2 != 1 else 0
    y_ratio = float(h1 - 1) / (h2 - 1) if h2 != 1 else 0

    for y2 in range(h2):
        for x2 in range(w2):
            # Find the coordinates in the original image
            x1 = x2 * x_ratio
            y1 = y2 * y_ratio

            # Get the integer parts of the coordinates
            x1_floor = int(x1)
            y1_floor = int(y1)

            # Get the fractional parts of the coordinates
            x1_frac = x1 - x1_floor
            y1_frac = y1 - y1_floor

            # Ensure we don't go out of bounds
            x1_ceil = min(x1_floor + 1, w1 - 1)
            y1_ceil = min(y1_floor + 1, h1 - 1)

            # Perform bilinear interpolation
            top_left = image[y1_floor][x1_floor]
            top_right = image[y1_floor][x1_ceil]
            bottom_left = image[y1_ceil][x1_floor]
            bottom_right = image[y1_ceil][x1_ceil]

            top = top_left * (1 - x1_frac) + top_right * x1_frac
            bottom = bottom_left * (1 - x1_frac) + bottom_right * x1_frac

            resized_image[y2][x2] = top * (1 - y1_frac) + bottom * y1_frac

    return resized_image


def heat_to_color(heat: float) -> str:
    heat_min = 22
    heat_max = 33
    heat_mapped = 256 * (heat - heat_min) / (heat_max - heat_min)
    heat_clamped = int(min(255, max(0, heat_mapped)))
    col = f"{heat_clamped:02X}0000"
    return col


# cam setup
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
    cam_mat = [[frame[cam_w * y + x] for y in range(cam_h)] for x in range(cam_w)][::-1]
    cam_mat_resized = resize(cam_mat, screen_w, screen_h)
    col_mat = [
        [heat_to_color(cam_mat_resized[y][x]) for x in range(screen_w)]
        for y in range(screen_h)
    ]
    paint(col_mat)
