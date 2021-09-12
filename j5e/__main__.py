import signal, sys

from j5e.Hypervisor import Hypervisor




def signal_handler(sig, frame):
    print("\nGame closing")
    global hypervisor
    hypervisor.stop()
    sys.exit(0)



if __name__ == "__main__":
    global hypervisor
    signal.signal(signal.SIGINT, signal_handler)

    hypervisor = Hypervisor()
    hypervisor.start()
    print("Game started")

    signal.pause()


hypervisor = None
