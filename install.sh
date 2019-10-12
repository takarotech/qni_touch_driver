#!/bin/bash

#-> Make sure we don't run as root
if (( EUID == 0 )); then
	echo 'Please run without sudo!' 1>&2
	exit 1
fi

#-> Go to the directory of this script
cd "$(dirname "${BASH_SOURCE[0]}")"

#-> Install i2c package
sudo -H pip3 install smbus2

#-> Enable i2c, 
sudo raspi-config nonint do_i2c 0

#-> Add to autostart
echo @$(pwd)/run_qni_touch_driver.sh >> $HOME/.config/lxsession/LXDE-pi/autostart
