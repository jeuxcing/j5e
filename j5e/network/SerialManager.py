import subprocess as sp
import time
from threading import Thread
import serial


class SerialManager(Thread):

    def __init__(self, serial_id, verbose=False):
        super().__init__()
        self.arduinos = {}
        self.current_port = 5555
        self.ended = False
        self.serial_id = serial_id
        self.redirector = None
        self.on_event_functions = []
        self.verbose = verbose
        self.list_arduinos()


    def add_handeling_function(self, function):
        self.on_event_functions.append(function)


    # def list_arduinos(self):
    #     # sys call to read kernel messages
    #     dmesg = ["sudo", "dmesg"]
    #     val = str(sp.run(dmesg, capture_output=True))
    #     # split messages related to arduino
    #     lines = val.split("\\n")
    #     for idx, line in enumerate(lines):
    #         if ("USB ACM device" in line):
    #             port = line.split(":")[-2][1:]
    #             serial = lines[idx-1].split(" ")[-1]
    #             self.arduinos[serial] = port

    #     print(self.arduinos)


    def list_arduinos(self):
        # sys call to read kernel messages
        dmesg = ["sudo", "dmesg"]
        val = str(sp.run(dmesg, capture_output=True))
        # split messages related to arduino
        lines = val.split("\\n")
        for idx, line in enumerate(lines[1:]):
            idx += 1
            # Device connection
            if "New USB device found" in line:
                spl = line.split(" ")
                idVendor = idProduct = ""
                for word in spl:
                    if word.startswith("idVendor"):
                        idVendor = word.split("=")[1][:-1]
                    elif word.startswith("idProduct"):
                        idProduct = word.split("=")[1][:-1]

                # verif arduino
                if idVendor != "1a86" or idProduct != "7523":
                    continue

                # device number
                dev_num_line = lines[idx-1]
                position = dev_num_line.find("USB device number ")
                if position == -1:
                    continue
                position += len("USB device number ")
                device_id = dev_num_line[position:].split(" ")[0]

                # port name
                port_line = lines[idx+4]
                position = port_line.find("attached to ")
                if position == -1:
                    continue
                position += len("attached to ")
                port_name = port_line[position:].split(" ")[0]

                # register
                self.arduinos[device_id] = port_name
                print("Added USB device ", device_id, " from port ", port_name)

            # Defvice disconnection
            elif "USB disconnect" in line:
                position = line.find("device number ")
                if position == -1:
                    continue
                position += len("device number ")
                device_id = line[position:].split(" ")[0]
                
                # remove from dict
                if device_id in self.arduinos:
                    print("Removing USB device ", device_id, " from port ", self.arduinos[device_id])
                    del self.arduinos[device_id]

        # Start connections
        for serial_id in list(self.arduinos.keys()):
            ser = serial.Serial(f'/dev/{self.arduinos[serial_id]}', timeout=0.1)
            print("Reading serial from port ", f'/dev/{self.arduinos[serial_id]}')
            val = ser.read()
            print(val)

            if val != self.serial_id:
                del self.arduinos[serial_id]
            else:
                print("val length", len(val))
                ser.write(val)
            ser.close()
        print("Arduinos list = ")
        print(self.arduinos)


    def redirect(self, serial, port):
        cmd = ["sudo", "socat", f"/dev/{self.arduinos[serial]},b115200,raw,echo=0", f"tcp-listen:{port}"]
        if self.verbose:
            print(" ".join(cmd))
        self.redirector = sp.Popen(cmd)


    def run(self):
        while not self.ended:
            # find the arduino
            self.list_arduinos()
            if self.serial_id not in self.arduinos:
                if self.verbose:
                    print(f"Arduino {self.serial_id} not plugged")
                time.sleep(1)
                continue

            # redirect the flux
            self.redirect(self.serial_id, self.current_port)
            for function in self.on_event_functions:
                function("connect", [self.serial_id, self.current_port])
            while self.redirector.poll() is None and not self.ended:
                time.sleep(1)
            for function in self.on_event_functions:
                function("disconnect", [self.serial_id, self.current_port])

            # change port
            if not self.ended:
                if self.verbose:
                    print(f"Port changed to {self.current_port}")
                self.current_port = 5555 + ((self.current_port + 46) % 100)
                time.sleep(1)
        if self.verbose:
            print("Serial Closed")


    def stop(self):
        self.ended = True
        if self.redirector is not None:
            sp.run(["sudo", "pkill", "-9", "socat"])
