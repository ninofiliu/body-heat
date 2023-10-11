#!/bin/sh
printf "i2c frequency: %dHz\n" 0x$(xxd -p /sys/class/i2c-adapter/i2c-1/of_node/clock-frequency)
