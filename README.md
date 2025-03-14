# Body heat

An interactive sculpture by [Nino Filiu](https://instagram.com/nino.filiu/) and [Paul Créange](https://www.instagram.com/paulcreange/)

Add these to `/boot/config.txt` so as to run I2C over GPIO (not needed for single setup)

```txt
dtoverlay=i2c-gpio,bus=6,i2c_gpio_delay_us=1,i2c_gpio_sda=6,i2c_gpio_scl=13
dtoverlay=i2c-gpio,bus=5,i2c_gpio_delay_us=1,i2c_gpio_sda=8,i2c_gpio_scl=5
dtoverlay=i2c-gpio,bus=4,i2c_gpio_delay_us=1,i2c_gpio_sda=10,i2c_gpio_scl=9
dtoverlay=i2c-gpio,bus=3,i2c_gpio_delay_us=1,i2c_gpio_sda=27,i2c_gpio_scl=22
```

and add this to augment baud rate

```txt
dtparam=i2c_arm_baudrate=800000
```

then reboot

Use apt to install optimized python packages, as they come pre-built. Using pip builds them locally and it can takes - literally - hours.

```sh
apt install python3-numpy python3-matplotlib
pip install adafruit_mlx90640 adafruit-circuitpython-tca9548a
```

```sh
pip install --break-system-packages adafruit-circuitpython-mlx90640
```

Setup the chaleur service so that it runs on startup:

```sh
sudo cp body-heat.service /lib/systemd/system/.
sudo chmod 644 /lib/systemd/system/body-heat.service
sudo systemctl enable body-heat.service
```

then reboot

Check that it's running:

```sh
systemctl status body-heat
journalctl -u body-heat.service -f
```

# Pinout
        
- pi.gnd cam.gnd(black)
- pi.5v cam.vin(red)
- pi.gpio02 cam.sda(blue)
- pi.gpio04 cam.scl(yellow)

- pi.gnd pixel.gnd
- pi.gpio18 pixel.din(green,middle)

- supply.l power.l(brown)
- supply.n power.n(yellow)
- supply.gnd power.gnd(yellow/green)
- supply.v- pixel.gnd(white)
- supply.v+ pixel.vin(red)
- supply.v- diod supply.v+

# SSH

username: pi
pwd: pi

from pi:

```sh
# ssh setup
ssh-keygen -t ed25519 -C "filiunino@gmail.com"
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

from computer:

```sh
# list all addresses where the pi could be configured
arp -a
```

setup from ssh'd pi:

```sh
# install deps
sudo pip3 install --break-system-packages Adafruit-Blinka Adafruit-Blinka-Raspberry-Pi5-Neopixel
```
