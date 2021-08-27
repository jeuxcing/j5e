#! /usr/bin/env python

"""Main for the arduino connection."""

import time
from collections import deque, defaultdict
import logging
import sys

from .serial_device import SerialDevice, list_devices_connected
import json

messages_from_devices = deque()
messages_to_devices = defaultdict(lambda: deque(maxlen=1000))
messages_exceptions = deque()
connected_devices = {}

HOSTNAME = "lovelace"

logger = logging.getLogger('root')
FORMAT = (
    '[%(asctime)s :: %(levelname)s '
    '%(filename)s:%(lineno)s - %(funcName)10s() ]'
    ' :: %(message)s'
)

logging.basicConfig(format=FORMAT)
logger.setLevel(logging.INFO)

def _main():
    serial_ids = ["758333139333512021D2"]
    ports = list(list_devices_connected(serial_ids))
    for port in ports:
        if port in connected_devices:
            continue

        logger.info(f"Port: {port}")
        serial_device = SerialDevice(
            port,
            messages_from_devices,
            messages_to_devices,
            messages_exceptions
        )

        serial_device.start()
        connected_devices[port] = serial_device

    logger.info(connected_devices)


def main():
    """Manage the devices list."""
    _main()

    while messages_exceptions:
        broken_device = messages_exceptions.pop()
        print("Break", str(broken_device))
        print(messages_from_devices)
        connected_devices.pop(broken_device.port)

    #messages_from_devices.append(
    #    ["status", HOSTNAME, "connected devices", json.dumps({i: str(connected_devices[i]) for i in connected_devices})]
    #)
    logger.info(f"status {HOSTNAME} connected devices {json.dumps({i: str(connected_devices[i]) for i in connected_devices})}")

if __name__ == '__main__':
    while 1:
        try:
            main()
        except Exception as e:
            logger.exception(e)
        time.sleep(1)
