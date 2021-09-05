from j5e.network.SerialManager import SerialManager
from j5e.network.SocketClient import SocketClient


class Networks:

    wall_serial = "75833313933351104032"


    def __init__(self):
        # Init connections
        self.serial_manager = SerialManager(Networks.wall_serial)
        self.socket_client = SocketClient()

        # event handling
        self.serial_manager.add_handeling_function(self.socket_client.port_event)

        # run threads
        self.serial_manager.start()
        self.socket_client.start()


    def stop(self):
        self.socket_client.stop()
        self.serial_manager.stop()