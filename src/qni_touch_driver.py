#!/usr/bin/python3

import time
import logging
import capacitive_electrodes

from qni_core import logger, config


class QniTouchDriver(object):
    _logger = logging.getLogger('qni_touch_driver')
    UPDATE_DELAY = 0.1

    def __init__(self):
        logger.config_logger()
        self.electrodes = capacitive_electrodes.CapacitiveElectrodes(
            config.ELECTRODES_SIZE, config.TILE_SIZE, config.MPR121_LAYOUT)
        self.electrodes.init()

    def mainloop(self):
        while True:
            self.electrodes.update()
            time.sleep(self.UPDATE_DELAY)


def main():
    app = QniTouchDriver()
    app.mainloop()


if __name__ == '__main__':
    main()
