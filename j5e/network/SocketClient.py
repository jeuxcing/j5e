import socket
import time
from threading import Thread


class SocketClient(Thread):

    def __init__(self, verbose=False):
        super().__init__()

        self.port = 6000
        self.stopped = False
        self.mailbox = []
        self.msg_handlers = []
        self.verbose = verbose


    def port_event(self, event_name, attrs):
        if event_name == "connect":
            self.port = attrs[1]


    def register_msg_handler(self, function):
        self.msg_handlers.append(function)


    def send(self, msg):
        print(len(msg), msg)
        self.mailbox.append(msg)


    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            while not self.stopped:
                try:
                    current_port = self.port
                    sock.setblocking(1)
                    sock.connect(("127.0.0.1", current_port))
                    sock.settimeout(0.01)
                    if self.verbose:
                        print(f"Socket opened on port {current_port}")
                    while current_port == self.port and not self.stopped:
                        # receive messages
                        data = None
                        try:
                            packet_size = sock.recv(1)
                            data = sock.recv(packet_size)
                        except socket.timeout:
                            pass

                        # Transmit data to handlers
                        if data is not None:
                            for function in self.msg_handlers:
                                function(data)

                        # send messages from the mailbox
                        if len(self.mailbox) > 0:
                            messages = self.mailbox
                            self.mailbox = []
                            sock.setblocking(1)
                            for msg in messages:
                                if self.verbose:
                                    print(f"sending: {msg}")
                                sock.send(len(msg))
                                sock.send(msg)
                            sock.settimeout(0.01)

                except ConnectionRefusedError:
                    if self.verbose:
                        print(f"Connexion refused on port {self.port}")
                    time.sleep(1)
                    continue
        if self.verbose:
            print("Socket closed")

    def stop(self):
        self.stopped = True