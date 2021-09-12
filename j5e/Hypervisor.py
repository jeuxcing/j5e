import time
from j5e.network.Networks import Networks
from j5e.hardware.led_strip import Grid


class Hypervisor:

    def __init__(self):
        self.network = Networks()
        # Time for all the networks to init
        time.sleep(3)
        self.grid = Grid(self.network)


    def start(self):
        time.sleep(2)
        # self.network.send_to_wall(b"Hello")
        # time.sleep(3)
        print("force closing")
        self.network.stop()
