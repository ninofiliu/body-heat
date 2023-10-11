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
pip install adafruit_mlx90640 adafruit-circuitpython-tca9548a
```

Setup the chaleur service so that it runs on startup:

```sh
sudo cp chaleur.service /lib/systemd/system/.
sudo chmod 644 /lib/systemd/system/chaleur.service
sudo systemctl enable chaleur.service
reboot
```

Check that it's running:

```sh
systemctl status chaleur
journalctl -u chaleur.service -f
```
dtoverlay=i2c-gpio,bus=6,i2c_gpio_delay_us=1,i2c_gpio_sda=6,i2c_gpio_scl=13
dtoverlay=i2c-gpio,bus=5,i2c_gpio_delay_us=1,i2c_gpio_sda=8,i2c_gpio_scl=5
dtoverlay=i2c-gpio,bus=4,i2c_gpio_delay_us=1,i2c_gpio_sda=10,i2c_gpio_scl=9
dtoverlay=i2c-gpio,bus=3,i2c_gpio_delay_us=1,i2c_gpio_sda=27,i2c_gpio_scl=22
