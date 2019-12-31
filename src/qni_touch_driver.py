#!/usr/bin/python3

import time
import logging
import RPi.GPIO as GPIO
import capacitive_electrodes

from qni_core import logger, config


class QniTouchDriver(object):
    _logger = logging.getLogger('qni_touch_driver')
    UPDATE_DELAY = 0.1
    LED_ENABLE_PIN = 4

    def __init__(self):
        logger.config_logger()
        self.electrodes = capacitive_electrodes.CapacitiveElectrodes(
            config.ELECTRODES_SIZE, config.TILE_SIZE, config.MPR121_LAYOUT)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.LED_ENABLE_PIN, GPIO.OUT)
        GPIO.output(self.LED_ENABLE_PIN, GPIO.LOW)
        self.electrodes.init()
        GPIO.setup(self.LED_ENABLE_PIN, GPIO.IN)

    def mainloop(self):
        while True:
            self.electrodes.update()
            time.sleep(self.UPDATE_DELAY)


def main():
    app = QniTouchDriver()
    app.mainloop()


if __name__ == '__main__':
    main()
