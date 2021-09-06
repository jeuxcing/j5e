from j5e.network.SerialManager import SerialManager
from j5e.network.SocketClient import SocketClient


class Networks:

    # To know the serial number of an arduino (linux only):
    # 1 - plug the arduino to the computer usb
    # 2 - sudo dmesg
    # 3 - read the last "SerialNumber"

    # The following 2 values needs to be changed regarding the arduino used
    wall_serial = "75833313933351104032"
    ctrl_serial = "758303339383511090A1"


    def __init__(self):
        # Init connections to the wall
        self.wall_serial_manager = SerialManager(Networks.wall_serial)
        self.wall_socket_client = SocketClient()
        # event handling
        self.wall_serial_manager.add_handeling_function(self.wall_socket_client.port_event)

        # Init connections to the controller
        self.ctrl_serial_manager = SerialManager(Networks.ctrl_serial)
        self.ctrl_socket_client = SocketClient()
        # event handling
        self.ctrl_serial_manager.add_handeling_function(self.wall_socket_client.port_event)

        # run threads
        self.wall_serial_manager.start()
        self.wall_socket_client.start()
        self.ctrl_serial_manager.start()
        self.ctrl_socket_client.start()


    def send_to_wall(self, msg):
        self.wall_socket_client.send(msg);


    def ctrl_msg_register(self, function):
        """ function is registered to be called when a message arrives
        """
        self.ctrl_socket_client.register_msg_handler(function)


    def stop(self):
        self.wall_socket_client.stop()
        self.wall_serial_manager.stop()