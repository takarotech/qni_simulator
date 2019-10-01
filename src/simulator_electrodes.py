from qni_core import electrodes


class SimulatorElectrodes(electrodes.EvElectrodesGrid):

    def __init__(self, grid_sizes, pixel_sizes, paws, led_map, mid_pixel):
        electrodes.EvElectrodesGrid.__init__(self, grid_sizes, pixel_sizes, True)
        self.paws = paws
        for i in self.electrodes:
            i.mid_point = [led_map[p] - mid_pixel for p in i.mid_pixel]

    def _send(self):
        mt_points = []
        self.paws.update_window_mask()
        for i in self.electrodes:
            if self.paws.window_mask.get_at(i.mid_point):
                mt_points.append(i.grid_indexes)
        if self.last_mt_points != mt_points:
            self.last_mt_points = mt_points.copy()
            self.ev_touch.update(mt_points)
