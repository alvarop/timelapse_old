README.md

# Raspberry Pi Timelapse Setup Instructions

(You need a raspberry pi and a USB webcam)

Download Raspbian Lite from https://www.raspberrypi.org/downloads/raspbian/

Write image to SD card https://www.raspberrypi.org/documentation/installation/installing-images/README.md
(I used https://etcher.io/)

On the SD card (while it's still mounted to your main system):

echo "
network={
  ssid=\"testing\"
  psk=\"testingPassword\"
}" | sudo tee --append etc/wpa_supplicant/wpa_supplicant.conf

Also:
sudo touch /boot/ssh

Insert SD card to Raspberry Pi and power up

ssh pi@ip.ad.dr.ess

`sudo ln -sf /usr/share/zoneinfo/PST8PDT /etc/localtime`

`sudo reboot`

(reconnect)

`sudo apt update`

`sudo apt install python3-pip tmux fswebcam ipython3 git libimage-exiftool-perl`

`pip3 install astral`

`git clone https://github.com/alvarop/timelapse.git`
