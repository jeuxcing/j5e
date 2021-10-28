import subprocess as sp
import sys
import serial
import time
from threading import Thread


class SerialManager(Thread):

    def __init__(self, serial_id, verbose=False):
        super().__init__()
        self.arduinos = {}
        self.list_arduinos()
        # self.current_port = 5555
        self.ended = False
        self.serial_id = serial_id
        self.serial = None
        self.inbox = []
        self.outbox = []
        # self.redirector = None
        self.on_event_functions = []
        self.verbose = verbose


    def add_handeling_function(self, function):
        self.on_event_functions.append(function)


    def send_msg(self, msg):
        self.outbox.append(msg)


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

        # print(self.arduinos)


    # def redirect(self, serial, port):
    #     cmd = ["sudo", "socat", f"/dev/{self.arduinos[serial]},b115200,raw,echo=0", f"tcp-listen:{port}"]
    #     if self.verbose:
    #         print(" ".join(cmd))
    #     self.redirector = sp.Popen(cmd)


    def run(self):
        acknowledged = True
        while not self.ended:
            # find the arduino
            if self.serial == None:
                self.list_arduinos()
                # when arduino absent
                if self.serial_id not in self.arduinos:
                    if self.verbose:
                        print(f"Arduino {self.serial_id} not plugged")
                    time.sleep(1)
                    continue

                # Opent the serial
                try:
                    self.serial = serial.Serial(f"/dev/{self.arduinos[self.serial_id]}", baudrate=115200)
                except serial.serialutil.SerialException:
                    self.serial = None
            else:
                try:
                    print("<", len(self.inbox), "   >", len(self.outbox))
                    # Write to device
                    if acknowledged and len(self.outbox) > 0:
                        msg = bytes([len(self.outbox[0])]) + self.outbox[0]
                        if self.verbose:
                            print("send:", msg)
                        self.last_send = time.time()
                        self.serial.write(msg)
                        self.serial.flush()
                        acknowledged = False
                    elif not acknowledged and time.time() - self.last_send > .05:
                        acknowledged = True

                    # Read from device
                    for i in range(min(100, self.serial.in_waiting)):
                        self.inbox.append(self.serial.read())

                    if len(self.inbox) > 0:
                        size = int.from_bytes(self.inbox[0], "big")
                        if size <= len(self.inbox) - 1:
                            msg = self.inbox[1:size+1]
                            self.inbox = self.inbox[size+1:]

                            if self.verbose:
                                print("recv:", msg)

                            if not acknowledged and int.from_bytes(msg[0], "big") == 0xFF:
                                if self.verbose:
                                    print("ack [latency", time.time() - self.last_send, "]")
                                self.outbox = self.outbox[1:]
                                acknowledged = True
                                continue

                            for function in self.on_event_functions:
                                function("msg", msg)
                except serial.serialutil.SerialException:
                    self.serial = None
                except Exception as e:
                    self.serial = None
                    print(e, file=sys.stderr)

            time.sleep(0.001)
        if self.verbose:
            print("Serial Closed")

    # def run(self):
    #     while not self.ended:
    #         # find the arduino
    #         self.list_arduinos()
    #         if self.serial_id not in self.arduinos:
    #             if self.verbose:
    #                 print(f"Arduino {self.serial_id} not plugged")
    #             time.sleep(1)
    #             continue

    #         # redirect the flux
    #         self.redirect(self.serial_id, self.current_port)
    #         for function in self.on_event_functions:
    #             function("connect", [self.serial_id, self.current_port])
    #         while self.redirector.poll() is None and not self.ended:
    #             time.sleep(1)
    #         for function in self.on_event_functions:
    #             function("disconnect", [self.serial_id, self.current_port])

    #         # change port
    #         if not self.ended:
    #             if self.verbose:
    #                 print(f"Port changed to {self.current_port}")
    #             self.current_port = 5555 + ((self.current_port + 46) % 100)
    #             time.sleep(1)
    #     if self.verbose:
    #         print("Serial Closed")


    def stop(self):
        self.ended = True
        if self.serial is not None:
            self.serial.close()
        # if self.redirector is not None:
        #     sp.run(["sudo", "pkill", "-9", "socat"])
