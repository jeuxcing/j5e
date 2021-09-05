import subprocess as sp
import time
from threading import Thread


class SerialManager(Thread):

    def __init__(self, serial_id):
        super().__init__()
        self.arduinos = {}
        self.list_arduinos()
        self.current_port = 5555
        self.ended = False
        self.serial_id = serial_id
        self.redirector = None
        self.on_event_functions = []


    def add_handeling_function(self, function):
        self.on_event_functions.append(function)


    def list_arduinos(self):
        # sys call to read kernel messages
        dmesg = ["sudo", "dmesg"]
        val = str(sp.run(dmesg, capture_output=True))
        # split messages related to arduino
        lines = val.split("\\n")
        for idx, line in enumerate(lines):
            if ("USB ACM device" in line):
                port = line.split(":")[-2][1:]
                serial = lines[idx-1].split(" ")[-1]
                self.arduinos[serial] = port


    def redirect(self, serial, port):
        cmd = ["sudo", "socat", f"/dev/{self.arduinos[serial]},b115200,raw,echo=0", f"tcp-listen:{port}"]
        print(" ".join(cmd))
        self.redirector = sp.Popen(cmd)


    def run(self):
        while not self.ended:
            # find the arduino
            self.list_arduinos()
            if self.serial_id not in self.arduinos:
                print(f"Arduino {self.serial_id} not plugged")
                time.sleep(1)
                continue

            # redirect the flux
            self.redirect(self.serial_id, self.current_port)
            for function in self.on_event_functions:
                function("connect", [self.serial_id, self.current_port])
            while self.redirector.poll() is None:
                time.sleep(1)
            for function in self.on_event_functions:
                function("disconnect", [self.serial_id, self.current_port])

            # change port
            if not self.ended:
                print(f"Port changed to {self.current_port}")
                self.current_port = 5555 + ((self.current_port + 46) % 100)
                time.sleep(1)


    def stop(self):
        self.ended = True
        if self.redirector is not None:
            sp.run(["sudo", "pkill", "-9", "socat"])
