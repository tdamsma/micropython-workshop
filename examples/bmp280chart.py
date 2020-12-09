from display import display
from st7789 import (
    BLUE,
    RED,
    YELLOW,
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
data_t = [t] * WIDTH
data_p = [p] * WIDTH
data_h = [h] * WIDTH
scaled_t = [0] * WIDTH
scaled_p = [0] * WIDTH
scaled_h = [0] * WIDTH
while True:
    t, p, h = sensor.read_compensated_data()
    j = 0 if i == WIDTH - 1 else i + 1
    data_t[j] = t
    data_p[j] = p
    data_h[j] = h
    min_t = min(data_t)
    scale_t = HEIGHT / ((max(data_t) - min_t) + 0.1)
    min_p = min(data_p)
    scale_p = HEIGHT / ((max(data_p) - min_p) + 0.1)
    min_h = min(data_h)
    scale_h = HEIGHT / ((max(data_h) - min_h) + 0.1)
    for n in range(WIDTH):
        v = int((data_t[(j + n) % WIDTH] - min_t) * scale_t)
        display.pixel(scaled_t[n], n, 0)
        display.pixel(v, n, YELLOW)
        scaled_t[n] = v
        v = int((data_p[(j + n) % WIDTH] - min_p) * scale_p)
        display.pixel(scaled_p[n], n, 0)
        display.pixel(v, n, BLUE)
        scaled_p[n] = v
        v = int((data_h[(j + n) % WIDTH] - min_h) * scale_h)
        display.pixel(scaled_h[n], n, 0)
        display.pixel(v, n, RED)
        scaled_h[n] = v
    i = j

    display.draw_text(10, 0, "{: 5.2f} C".format(data_t[j]), color=YELLOW)
    display.draw_text(30, 0, "{: 5.2f} mBar".format(data_p[j]), color=BLUE)
    display.draw_text(50, 0, "{: 5.2f} %".format(data_h[j]), color=RED)
    time.sleep(0.01)

