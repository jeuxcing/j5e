from j5e.network.SerialManager import SerialManager

class Networks:

    wall_serial = "75833313933351104032"

    def __init__(self):
        self.serial_manager = SerialManager()
        self.serial_manager.redirect(Networks.wall_serial)