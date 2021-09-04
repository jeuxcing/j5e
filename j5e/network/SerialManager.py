import subprocess as sp


class SerialManager:

    def __init__(self):
        self.arduinos = {}
        self.list_arduinos()

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


    def redirect(self, serial):
        cmd = ["sudo", "socat", f"/dev/{self.arduinos[serial]},b115200,raw,echo=0", "tcp-listen:5555"]
        print(" ".join(cmd))
        val = sp.run(cmd, capture_output=True)
        print(val)
        print("ENDED")


    def start(self):
        self.list_arduinos()
        if len(self.arduinos) == 0:
            return

        serial = next(iter(self.arduinos.keys()))
        self.redirect(serial)

