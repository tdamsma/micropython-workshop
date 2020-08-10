from machine import Pin, ADC
from display import display

while True:
    for i, p in enumerate(range(32, 40)):
        display.draw_text(i * 10, 0, "{}: {: 5d}".format(p, ADC(Pin(p)).read()))
