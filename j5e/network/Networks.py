from j5e.network.SerialManager import SerialManager

class Networks:

    wall_serial = "75833313933351104032"

    def __init__(self):
        self.serial_manager = SerialManager(Networks.wall_serial)
        self.serial_manager.start()

    def stop(self):
        self.serial_manager.stop()