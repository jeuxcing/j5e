import time
from j5e.network.Networks import Networks


class Hypervisor:

    def __init__(self):
        self.network = Networks()


    def start(self):
        time.sleep(5)
        print("pouet")
        self.network.stop()
