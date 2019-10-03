#!/bin/bash

#-> Make sure we don't run as root
if (( EUID == 0 )); then
   echo 'Please run without sudo!' 1>&2
   exit 1
fi

#-> Install i2c package
sudo -H pip3 install smbus2

#-> Enable i2c, 
sudo raspi-config nonint do_i2c 0
