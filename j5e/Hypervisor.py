import time
from j5e.network.Networks import Networks
from j5e.hardware.led_strip import Grid, GridDims as gd


class Hypervisor:

    def __init__(self):
        self.network = Networks()
        # Time for all the networks to init
        time.sleep(3)
        self.grid = Grid(self.network)


    def start(self):
        self.grid.set_color(gd.ROW, 0, 0, 1, (20, 0, 0))
        

    def stop(self):
        self.network.stop()
