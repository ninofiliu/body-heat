#!/bin/sh
echo "adding service..."
sudo cp body-heat.service /lib/systemd/system/.
sudo chmod 644 /lib/systemd/system/body-heat.service
echo "enabling service..."
sudo systemctl enable body-heat.service
echo "service added and enabled"
