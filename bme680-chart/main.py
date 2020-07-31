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

from machine import Pin
from i2c_adapter import I2CAdapter

i2c = I2CAdapter(sda=Pin(22), scl=Pin(21))
import bme680
import time

sensor = bme680.BME680(i2c_device=i2c, i2c_addr=0x77)
display.fill(0)
WIDTH = 240
HEIGHT = 135
MARGIN = 10
i = 0
assert sensor.get_sensor_data()

data_temp = [sensor.data.temperature] * WIDTH
scaled_temp = [0] * WIDTH
data_humi = [sensor.data.humidity] * WIDTH
scaled_humi = [0] * WIDTH
while True:
    if not sensor.get_sensor_data():
        continue
    if i == WIDTH - 1:
        j = 0
    else:
        j = i + 1
    data_temp[j] = sensor.data.temperature
    data_humi[j] = sensor.data.humidity
    m_temp = min(data_temp)
    scale_temp = (HEIGHT - MARGIN) / ((max(data_temp) - m_temp) + 0.01)
    m_humi = min(data_humi)
    scale_humi = (HEIGHT - MARGIN) / ((max(data_humi) - m_humi) + 0.01)

    for n in range(WIDTH):
        v = int((data_temp[(j + n + 1) % WIDTH] - m_temp) * scale_temp) + MARGIN
        display.pixel(scaled_temp[n], n, 0)
        display.pixel(v, n, YELLOW)
        scaled_temp[n] = v

        v = int((data_humi[(j + n + 1) % WIDTH] - m_humi) * scale_humi) + MARGIN
        display.pixel(scaled_humi[n], n, 0)
        display.pixel(v, n, BLUE)
        scaled_humi[n] = v

    i = j

    display.draw_text(0, 0, "{: 5.2f} C".format(data_temp[j]), color=YELLOW)
    display.draw_text(0, 180, "{: 5.2f} %".format(data_temp[j]), color=BLUE)
