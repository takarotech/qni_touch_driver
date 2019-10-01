import mpr121
import i2c_mux

from qni_core import electrodes, utils


class CapacitiveElectrodes(electrodes.EvElectrodesGrid):

    def __init__(self, grid_sizes, pixel_sizes, mpr121_map):
        electrodes.EvElectrodesGrid.__init__(self, grid_sizes, pixel_sizes, True)
        self.mprs = []
        elec_count = 0
        for mux_addr, mux_idx, dev_addr, elec_map in mpr121_map:
            elec_map_len = len(elec_map)
            dev = i2c_mux.MuxI2c(
                mpr121.Mpr121._I2C_BASE_ADDRESS + dev_addr, mux_idx, mux_addr)
            mpr = mpr121.Mpr121(dev, elec_map_len)
            mpr.elec_map = elec_map
            elec_count += elec_map_len
            self.mprs.append(mpr)
        self._all_mprs_dev = utils._Atter()
        self._all_mprs_dev.read = self._all_mprs_read
        self._all_mprs_dev.write = self._all_mprs_write
        self.all_mprs = mpr121.Mpr121(self._all_mprs_dev, elec_map_len)
        self.all_mprs.config_regs()

    def _all_mprs_read(self, reg_address, size=1):
        return self.mprs[0]._dev.read(reg_address, size)

    def _all_mprs_write(self, reg_address, data):
        for mpr in self.mprs:
            mpr._dev.write(reg_address, data)

    def init(self):
        for mpr in self.mprs:
            mpr.config_regs()

    def _send(self):
        mt_points = []

        bitmasks = [mpr._dev.read(0x00, 1)[0] for mpr in self.mprs]
        for bitmask, mpr in zip(bitmasks, self.mprs):
            for i in mpr.elec_map:
                if (bitmask & 1):
                    mt_points.append(self.electrodes[i].grid_indexes)
                bitmask >>= 1

        if self.last_mt_points != mt_points:
            self.last_mt_points = mt_points.copy()
            self.ev_touch.update(mt_points)
