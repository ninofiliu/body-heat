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

## Strip

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

## Tableau

Power

- GND: pi5.gnd / esp32.gnd / shifter.gnd / led.gnd / cam.gnd
- 5V: pi5.5v / shifter.vb
- 5V psu: psu5.5v / esp32.5v
- 3V: pi5.3v / cam.vin(red) / shifter.va

Logic

- pi5.rx (gpio14,pin18) / esp32.tx0
- pi5.tx (gpio15,pin10) / esp32.rx0
- esp32.d16 / shifter.a1; shifter.b1 - r65ohms - led.do
- esp32.d23 / shifter.a2; shifter.b2 - r65ohms - led.bo
- shifter.va / shifter.oe
- cam.3v(red) / pi5.3v (pin1)
- cam.sda(blue) / pi5.gpio2(pin3)
- cam.scl(yellow) / pi5.gpio4(pin5)

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
pip3 install --break-system-packages adafruit-blinka adafruit-circuitpython-mlx90640
```
