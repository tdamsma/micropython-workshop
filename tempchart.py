from display import display
from st7789 import (
    BLUE,
    GREEN,
    RED,
    YELLOW,
    CYAN,
    MAGENTA,
    WHITE,
    BLACK,
    color565,
    map_bitarray_to_rgb565,
)

display.fill(0)
from machine import Pin, I2C
import bme280
import time

i2c = I2C(id=0, scl=Pin(22), sda=Pin(21))
print(i2c.scan())
sensor = bme280.BME280(i2c=i2c)

display.fill(0)
WIDTH = 240
HEIGHT = 135
i = 0

t, p, h = sensor.read_compensated_data()
data = [t] * WIDTH
scaled = [0] * WIDTH
while True:
    t, p, h = sensor.read_compensated_data()
    if i == WIDTH - 1:
        j = 0
    else:
        j = i + 1
    data[j] = t
    m = min(data)
    scale = HEIGHT / ((max(data) - m) + 0.1)
    for n in range(WIDTH):
        v = int((data[(j + n) % WIDTH] - m) * scale)
        display.pixel(scaled[n], n, 0)
        display.pixel(v, n, YELLOW)
        scaled[n] = v
    i = j
    time.sleep(0.01)

