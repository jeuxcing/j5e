import time
from j5e.network.Networks import Networks


class Hypervisor:

    def __init__(self):
        self.network = Networks()
        # Time for all the networks to init
        time.sleep(3)


    def start(self):
        time.sleep(2)
        self.network.send_to_wall(b"Hello")
        time.sleep(3)
        print("force closing")
        self.network.stop()
