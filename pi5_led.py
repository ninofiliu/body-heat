from pi5neo import Pi5Neo
import time

# Initialize the Pi5Neo class with 10 LEDs and an SPI speed of 800kHz
neo = Pi5Neo('/dev/spidev0.0', 678, 800)

for i in range(neo.num_leds):
  neo.set_led_color(i,0,5,0)
  neo.update_strip()
  # time.sleep(.1)
