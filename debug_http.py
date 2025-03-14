import requests
import json
import time

w = 43
h = 16
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


def paint(col_mat: list[list[str]]) -> None:
    for x, y in to_pop[::-1]:
        col_mat[y].pop(x)
    col_rev = [col_mat[i] if i % 2 == 0 else col_mat[i][::-1] for i in range(h)]
    col_arr = [col for line in col_rev for col in line]
    for chunk_start in range(0, nb_leds, chunk_size):
        col_chunk = col_arr[chunk_start : chunk_start + chunk_size]
        requests.post(
            "http://172.20.10.2/json",
            headers={"Content-Type": "application/json"},
            data=json.dumps(
                {"bri": 255, "seg": {"i": [chunk_start] + col_chunk}, "live": True}
            ),
        )


i = 0
while True:
    t0 = time.time()
    col_mat = [[f"{'10' if x == i else '00'}0000" for x in range(w)] for y in range(h)]
    paint(col_mat)
    i = (i + 1) % w
    t1 = time.time()
    print(f"{(t1-t0)*1000:.0f}ms ({1/(t1-t0):.2f}fps)")
