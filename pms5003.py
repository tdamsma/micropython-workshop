import uasyncio as asyncio
from machine import UART

uart = UART(2, 9600, rx=27)
uart.init(9600, bits=8, parity=None, stop=1)  # init with given parameters

from pms5003 import PMS5003
pms = PMS5003(uart)

import struct



while True:
    buffer = uart.read()
    if buffer is None or len(buffer) <= 17:
        continue
    frame = struct.unpack(">HHHHHHHHHHHHHH", buffer[4:])
    pm10_env = frame[3]
    print("pm10_env", pm10_env)

    # pm10_standard = frame[0]
    # pm25_standard = frame[1]
    # pm100_standard = frame[2]
    # pm10_env = frame[3]
    # pm25_env = frame[4]
    # pm100_env = frame[5]
    # particles_03um = frame[6]
    # particles_05um = frame[7]
    # particles_10um = frame[8]
    # particles_25um = frame[9]
    # particles_50um = frame[10]
    # particles_100um = frame[11]
