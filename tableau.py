import time
import board
import busio
import adafruit_mlx90640
import requests
import json


heat_min = 25
heat_max = 33
ramp = [
    # heatmap
    # (0.0, 0.66, 1, 5 / 256),
    # (0.5, 0.33, 1, 10 / 256),
    # (1, 0, 1, 128 / 256),
    # red gradient
    (0, 0, 1, 2 / 256),
    (0.8, 0, 1, 0.1),
    (1, 0, 1, 1),
]


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


wled_ip = "172.20.10.2"  # can sometimes be 4.3.2.1


def paint(col_mat: list[list[str]]) -> None:
    for x, y in to_pop[::-1]:
        col_mat[y].pop(x)
    col_rev = [col_mat[i] if i % 2 == 0 else col_mat[i][::-1] for i in range(screen_h)]
    col_arr = [col for line in col_rev for col in line]
    for chunk_start in range(0, nb_leds, chunk_size):
        col_chunk = col_arr[chunk_start : chunk_start + chunk_size]
        response = requests.post(
            f"http://{wled_ip}/json",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"bri": 255, "seg": {"i": [chunk_start] + col_chunk}}),
        )
        print(response.text)


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


def color_ramp(
    position: float, ramp: list[tuple[float, float, float, float]]
) -> tuple[float, float, float]:
    """
    Interpolates an HSV color from a color ramp based on the given position.

    :param position: A float between 0 and 1 representing the position on the color ramp.
    :param ramp: A list of tuples in the format (position, hue, saturation, value).
    :return: A tuple (hue, saturation, value) representing the interpolated color.
    """
    # Ensure the ramp is sorted by position
    ramp = sorted(ramp, key=lambda x: x[0])

    # Handle edge cases where position is outside the ramp
    if position <= ramp[0][0]:
        return ramp[0][1], ramp[0][2], ramp[0][3]
    if position >= ramp[-1][0]:
        return ramp[-1][1], ramp[-1][2], ramp[-1][3]

    # Find the two nearest points in the ramp
    for i in range(len(ramp) - 1):
        if ramp[i][0] <= position <= ramp[i + 1][0]:
            pos1, h1, s1, v1 = ramp[i]
            pos2, h2, s2, v2 = ramp[i + 1]
            break

    # Calculate the interpolation factor
    t = (position - pos1) / (pos2 - pos1)

    # Interpolate each component
    hue = h1 + t * (h2 - h1)
    saturation = s1 + t * (s2 - s1)
    value = v1 + t * (v2 - v1)

    return hue, saturation, value


def hsv_to_rgb(hsv: tuple[float, float, float]) -> tuple[int, int, int]:
    """
    Converts an HSV color to an RGB color.

    :param hsv: A tuple (hue, saturation, value) where:
        - hue is a float in the range [0, 1]
        - saturation is a float in the range [0, 1]
        - value is a float in the range [0, 1]
    :return: A tuple (red, green, blue) where each component is in the range [0, 255].
    """
    h, s, v = hsv
    if s == 0:
        # Achromatic (gray)
        r = g = b = int(v * 255)
        return r, g, b

    # Sector 0 to 5
    h *= 6.0
    i = int(h)
    f = h - i  # Fractional part of h
    p = v * (1.0 - s)
    q = v * (1.0 - s * f)
    t = v * (1.0 - s * (1.0 - f))

    if i == 0:
        r, g, b = v, t, p
    elif i == 1:
        r, g, b = q, v, p
    elif i == 2:
        r, g, b = p, v, t
    elif i == 3:
        r, g, b = p, q, v
    elif i == 4:
        r, g, b = t, p, v
    elif i == 5:
        r, g, b = v, p, q
    else:
        r, g, b = 0, 0, 0
        # raise ValueError("Hue value out of range")

    # Convert to 0-255 range
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)

    return r, g, b


def heat_to_color(heat: float) -> str:
    heat_normalized = min(1, max(0, (heat - heat_min) / (heat_max - heat_min)))

    hsv = color_ramp(heat_normalized, ramp)
    r, g, b = hsv_to_rgb(hsv)
    return f"{r:02X}{g:02X}{b:02X}"


# cam setup
i2c = busio.I2C(board.SCL, board.SDA)
mlx = adafruit_mlx90640.MLX90640(i2c)
print("MLX addr detected on I2C", [hex(i) for i in mlx.serial_number])
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_16_HZ
frame = [0] * 768

while True:
    try:
        mlx.getFrame(frame)
        cam_mat = [[frame[cam_w * y + x] for y in range(cam_h)] for x in range(cam_w)][
            ::-1
        ]
        cam_mat_resized = resize(cam_mat, screen_w, screen_h)
        col_mat = [
            [heat_to_color(cam_mat_resized[y][x]) for x in range(screen_w)]
            for y in range(screen_h)
        ]
        paint(col_mat)
    except Exception as e:
        print("Ignoring", e)
        continue
