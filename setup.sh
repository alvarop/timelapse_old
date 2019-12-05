#!/bin/bash

echo "Updating supervisor config setup"
sudo rm -f /etc/supervisor/conf.d/timelapse.conf
sudo cp timelapse.conf /etc/supervisor/conf.d/timelapse.conf

echo "restart supervisor"
sudo systemctl restart supervisor
