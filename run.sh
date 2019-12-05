#!/bin/bash

# Change these as necessary
v4l2-ctl -c focus_auto=0
v4l2-ctl -c focus_absolute=0

python3 timelapse.py --delay 600 --out_dir /home/pi/timelapse/photos/
# --daylight_only --out_dir /home/pi/timelapse/photos/
