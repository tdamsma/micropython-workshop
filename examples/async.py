from machine import Pin, I2C, UART
import bme280
import time
from display import display
import struct
from st7789 import BLUE, RED, YELLOW, BLACK, color565
from uasyncio import get_event_loop, sleep_ms
from uarray import array

# display.fill(BLACK)

# initialize sensors:
class Sensors:
    def __init__(self):
        i2c = I2C(id=0, scl=Pin(22), sda=Pin(21))
        bme = bme280.BME280(i2c=i2c)

        uart = UART(2, 9600, rx=27)
        uart.init(9600, bits=8, parity=None, stop=1)  # init with given parameters

        self._uart = uart
        self._bme = bme

    def _read_pms5003(self):
        buffer = self._uart.read()
        if buffer is None or len(buffer) < 32:
            self.pm10 = -1
        else:
            frame = struct.unpack(">HHHHHHHHHHHHHH", buffer[4:])
            self.pm10 = frame[3]  # pm10_env
        # flush
        # while self._uart.any():
        #     self._uart.read(self._uart.any())

    def _read_bme(self):
        t, p, h = self._bme.read_compensated_data()
        self.temperature = t
        self.pressure = p
        self.humidity = h

    def read(self):
        self._read_pms5003()
        self._read_bme()


sensors = Sensors()


class ButtonPressedCounter:
    DEBOUNCE_MS = 200
    last_increment = time.ticks_ms()
    counter = 0

    def __init__(self, button):
        button.irq(self.increment, trigger=Pin.IRQ_FALLING)

    def increment(self, _):
        now = time.ticks_ms()
        if time.ticks_diff(now, self.last_increment) > self.DEBOUNCE_MS:
            self.counter += 1
            # print(self.counter)
            self.last_increment = now


b1 = ButtonPressedCounter(Pin(0, Pin.IN))
b2 = ButtonPressedCounter(Pin(35, Pin.IN))


# every 2 seconds measure t, p, h, pm10

BASETICK = 250
WIDTH = 240


class Variable:

    scales = [1, 8, 15, 12]

    def __init__(
        self, source, no_data=-1, color=YELLOW, x=0, min=0, max=50, format="", title="",
    ):
        self.data = [array("f", [no_data] * WIDTH) for _ in self.scales]
        self.cursors = [0 for _ in self.scales]
        self.source = source
        self.no_data = no_data
        self.color = color
        self.x = x
        self.format = format
        self.min = min
        self.max = max
        self.title = title
        self.last_value = no_data

    async def measure_level(self, level):

        if level == 0:
            await sleep_ms(BASETICK)
            v = self.source()
            if v == self.no_data:
                v = self.last_value
            self.last_value = v
        else:
            sum = 0
            for _ in range(self.scales[level]):
                sum += await self.measure_level(level - 1)
            v = sum / self.scales[level]

        cursor = self.cursors[level]
        self.data[level][cursor] = v
        self.cursors[level] = (cursor + 1) % WIDTH

        return v

    async def update(self):
        await sleep_ms(800)
        while True:
            await self.measure_level(len(self.scales) - 1)


async def measure_sensors():
    await sleep_ms(700)
    while True:
        sensors.read()
        await sleep_ms(BASETICK)


class Plot:
    variable = None
    timescale = None
    chart = None
    plotted_values = array("h", [0] * WIDTH)
    HEIGHT = 90
    BOTTOM = 20

    def __init__(self, variables):
        self.variables = variables

    def draw_numbers(self):
        for v in self.variables:
            display.draw_text(0, v.x, v.format.format(v.last_value), color=v.color)

    def draw_chart(self):

        # get variable (and update title)
        v = self.variable
        t = self.timescale
        cursor = v.cursors[t]
        unrolled = array("f", v.data[t][(cursor + n) % WIDTH] for n in range(WIDTH))
        data = array("f", [x for x in unrolled if x != v.no_data])
        if len(data) > 0:
            d_min = max(v.min, min(data))
            d_max = min(v.max, max(data))
            if d_max - d_min < 0.1:
                d_max += 0.1
            display.draw_text(
                self.BOTTOM + self.HEIGHT, 0, v.format.format(d_max), color=v.color
            )
            display.draw_text(self.BOTTOM - 10, 0, v.format.format(d_min), color=v.color)

            scale = (d_max - d_min) / self.HEIGHT
            for k in range(len(data)):
                p = int((data[k] - d_min) / scale) + self.BOTTOM
                display.pixel(
                    min(
                        max(self.plotted_values[k], self.BOTTOM), self.BOTTOM + self.HEIGHT
                    ),
                    k,
                    BLACK,
                )
                display.pixel(
                    min(max(p, self.BOTTOM), self.BOTTOM + self.HEIGHT), k, v.color
                )
                self.plotted_values[k] = p
        for k in range(len(data), WIDTH):
            display.pixel(
                min(
                    max(self.plotted_values[k], self.BOTTOM), self.BOTTOM + self.HEIGHT
                ),
                k,
                BLACK,
            )
    def draw_title(self):

        # get variable (and update title)
        v = self.variables[b1.counter % len(self.variables)]
        if v != self.variable:
            self.variable = v
            self.timescale = None
            display.fill_rect(126, 0, 9, 100, BLACK)
            display.fill_rect(125, 0, 1, 100, v.color)
            display.fill_rect(self.BOTTOM + self.HEIGHT, 0, 10, 80, BLACK)
            display.fill_rect(self.BOTTOM - 10, 0, 10, 80, BLACK)
            display.draw_text(127, 0, "{}".format(v.title), color=v.color)

        t = b2.counter % len(v.scales)
        if t != self.timescale:
            self.timescale = t
            display.fill_rect(126, 100, 9, 140, BLACK)
            display.fill_rect(125, 100, 1, 140, v.color)
            n = 1
            while t >= 0:
                n *= v.scales[t]
                t -= 1
            unit = "seconds"
            count = n * 250 * 240 // 1000
            if count > 120:
                unit = "minutes"
                count //= 60
            if count > 120:
                unit = "hours"
                count //= 60

            display.draw_text(127, 100, "Last {} {}".format(count, unit), color=v.color)


PM10 = Variable(
    lambda: getattr(sensors, "pm10"),
    title="PM10",
    no_data=-1,
    color=color565(0, 255, 160),
    x=0,
    format="{: 3.0f}ppm",
    min=0,
    max=250,
)
Temperature = Variable(
    lambda: getattr(sensors, "temperature"),
    title="Temperature",
    no_data=20,
    color=YELLOW,
    x=35,
    format="{: 5.2f}C",
    min=0,
    max=40,
)
Pressure = Variable(
    lambda: getattr(sensors, "pressure"),
    title="Pressure",
    no_data=100_000,
    color=color565(255, 165, 0),
    x=80,
    format="{: 7.2f}mb",
    min=90_000,
    max=110_000,
)
Humidity = Variable(
    lambda: getattr(sensors, "humidity"),
    title="Humidity",
    no_data=50,
    color=color565(0, 165, 255),
    x=155,
    format="{: 5.2f}%",
    min=0,
    max=100,
)
variables = (PM10, Temperature, Pressure, Humidity)
plot = Plot(variables)


async def draw_numbers():
    await sleep_ms(1050)
    while True:
        plot.draw_numbers()
        await sleep_ms(500)


async def draw_title():
    await sleep_ms(1100)
    while True:
        plot.draw_title()
        await sleep_ms(500)


async def draw_chart():
    await sleep_ms(2150)
    while True:
        plot.draw_chart()
        await sleep_ms(2000)


l = get_event_loop()
l.create_task(measure_sensors())
for v in variables:
    l.create_task(v.update())

l.create_task(draw_numbers())
l.create_task(draw_chart())
l.create_task(draw_title())
l.run_forever()
