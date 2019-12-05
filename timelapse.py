#!/usr/bin/python3

from astral import Astral
import argparse
import sys
import os
import re
import time
import datetime
import pytz
import math

parser = argparse.ArgumentParser()
parser.add_argument('--resolution',
                    default='1920x1080',
                    help='Picture resulution')

parser.add_argument('--delay_s',
                    default=60,
                    type=int,
                    help='Delay between photos in seconds')

parser.add_argument('--daylight_only',
                    action='store_true',
                    help='Only take photos during the daylight hours')

parser.add_argument('--city',
                    default='San Francisco',
                    help='Major city for daylight calculation')

parser.add_argument('--out_dir',
                    default='photos/',
                    help='Output directory')

args = parser.parse_args()

index = 0

# Make sure output directory exists
if not os.path.exists(args.out_dir):
    print('Creating {}'.format(args.out_dir))
    os.makedirs(args.out_dir)

# Auto detect which image index is next
p = re.compile('img([0-9]+).jpg')
files = os.listdir(args.out_dir)
if len(files) > 0:
    match = p.match(max(files))
    if match:
        index = int(match.group(1)) + 1

print('Starting with index {}'.format(index))

def is_it_daytime(city_name):
    astr = Astral()
    astr.solar_depression = 'civil'

    city = astr[city_name]

    sun = city.sun(date=datetime.date.today(), local=True)

    sunrise = sun['sunrise']
    sunset = sun['sunset']
    now = datetime.datetime.fromtimestamp(
            time.time(),
            pytz.timezone(city.timezone))

    return sunrise < now < sunset

def sleep_until_sunrise(city_name):
    astr = Astral()
    astr.solar_depression = 'civil'

    city = astr[city_name]

    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    sun = city.sun(date=tomorrow, local=True)

    sunrise = sun['sunrise']
    now = datetime.datetime.fromtimestamp(
            time.time(),
            pytz.timezone(city.timezone))

    seconds_until_sunrise = math.ceil((sunrise - now).total_seconds())

    print('Sleeping until sunrise! ({} s)'.format(seconds_until_sunrise))

    time.sleep(seconds_until_sunrise)

while True:
    if args.daylight_only is False or is_it_daytime(args.city):
        filename = args.out_dir + 'img{:05d}.jpg'.format(index)

        # Manual focus (infinity)
        os.system('v4l2-ctl -c focus_auto=0')
        os.system('v4l2-ctl -c focus_absolute=0')

        cmd = [ 'fswebcam',
                '--no-banner',
                '-r ' + args.resolution,
                filename]
        os.system(' '.join(cmd))

        isodate = datetime.datetime.now().isoformat()

        cmd = [ 'exiftool',
                '-overwrite_original',
                '\'-datetimeoriginal={}\''.format(isodate),
                filename]
        os.system(' '.join(cmd))

        index += 1

        print('sleeping for {} seconds'.format(args.delay_s))
        time.sleep(args.delay_s)
    else:
        print("Night time, no_photo")
        sleep_until_sunrise(args.city)
