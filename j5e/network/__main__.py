
import subprocess as sp


def list_arduinos():
	arduinos = {}
	# sys call to read kernel messages
	dmesg = ["sudo", "dmesg"]
	val = str(sp.run(dmesg, capture_output=True))
	# split messages related to arduino
	lines = val.split("\\n")
	for idx, line in enumerate(lines):
		if ("USB ACM device" in line):
			port = line.split(":")[-2][1:]
			serial = lines[idx-1].split(" ")[-1]
			arduinos[serial] = port

	print(arduinos)


if __name__ == "__main__":
	# value = sp.run(["sudo dmesg  |grep  -B1 \"USB ACM device\"  | awk '/SerialNumber/{ser=$6} /cdc_acm/{dev=substr($5,1,length($5)-1);if (ser!="")print ser\" /dev/\"dev}' |uniq"])
	list_arduinos()

