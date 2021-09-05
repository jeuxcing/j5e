import socket
import time
from threading import Thread


class SocketClient(Thread):

    def __init__(self):
        super().__init__()

        self.port = 6000
        self.stopped = False
        self.mailbox = []


    def port_event(self, event_name, attrs):
        if event_name == "connect":
            self.port = attrs[1]


    def send(self, msg):
        self.mailbox.append(msg)


    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:

            while not self.stopped:
                try:
                    current_port = self.port
                    sock.setblocking(1)
                    sock.connect(("127.0.0.1", current_port))
                    sock.settimeout(0.01)
                    print(f"Socket opened on port {current_port}")
                    while current_port == self.port and not self.stopped:
                        # receive messages
                        try:
                            data = sock.recv(1024)
                            print(data)
                        except socket.timeout:
                            pass

                        # send messages
                        if len(self.mailbox) > 0:
                            messages = self.mailbox
                            self.mailbox = []
                            sock.setblocking(1)
                            for msg in messages:
                                print(f"sending: {msg}")
                                sock.send(msg)
                            sock.settimeout(0.01)

                except ConnectionRefusedError:
                    print(f"Connexion refused on port {self.port}")
                    time.sleep(1)
                    continue
        print("Socket closed")

    def stop(self):
        self.stopped = True