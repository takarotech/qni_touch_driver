#!/bin/bash

#-> Make sure we don't run as root
if (( EUID == 0 )); then
	echo 'Please run without sudo!' 1>&2
	exit 1
fi

#-> Make sure the driver is not running yet
QNI_TOUCH_DRIVER_BIN=./src/qni_touch_driver.py
if pgrep -f $QNI_TOUCH_DRIVER_BIN > /dev/null; then
	echo 'Please kill previous touch driver!' 1>&2
	exit 2
fi

#-> Go to the directory of this script
cd "$(dirname "${BASH_SOURCE[0]}")"

#-> Run qni_touch_driver with arguments
$QNI_TOUCH_DRIVER_BIN "$@"
