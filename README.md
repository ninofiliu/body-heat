# Chaleur

An interactive sculpture by [Nino Filiu](https://instagram.com/nino.filiu/) and [Paul Créange](https://www.instagram.com/paulcreange/)

This uses the mlx90640

Pinout:

- red: 3v3 (1)
- blue: gpio2 (3)
- yellow: gpio3 (5)
- black: gnd (9)

Use apt to install optimized python packages, as they come pre-built. Using pip builds them locally and it can takes - literally - hours.

```sh
apt install python3-numpy python3-matplotlib
pip install adafruit_mlx90640
```
