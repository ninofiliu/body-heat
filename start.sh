#!/bin/sh
set -x
echo "hello from the Body Heat Service"
whoami
su - pi
whoami
nmcli
cd /home/pi/body-heat
python tableau.py
