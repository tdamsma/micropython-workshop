import machine
import st7789
spi = machine.SPI(2, baudrate=40000000, polarity=1, sck=machine.Pin(18), mosi=machine.Pin(23))
display = st7789.ST7789(spi, 240, 240, reset=machine.Pin(4, machine.Pin.OUT), dc=machine.Pin(2, machine.Pin.OUT))
display.init()


import machine
import st7789
spi = machine.SPI(1, baudrate=40000000, polarity=1, sck=machine.Pin(18), mosi=machine.Pin(19))
display = st7789.ST7789(spi, 135, 240, reset=machine.Pin(23, machine.Pin.OUT), dc=machine.Pin(16, machine.Pin.OUT))
display.init()
display.pixel(120, 120, st7789.CYAN)



import machine
import st7789
spi = machine.SPI(2, baudrate=40000000, polarity=1, sck=machine.Pin(18), mosi=machine.Pin(23))
display = st7789.ST7789(spi, 135, 240, reset=machine.Pin(23, machine.Pin.OUT), dc=machine.Pin(16, machine.Pin.OUT))
display.init()
display.pixel(120, 120, st7789.CYAN)


st7789.ST7789.fill( st7789.CYAN)


import machine
spi = machine.SPI(1, baudrate=40000000, polarity=1, sck=machine.Pin(18), mosi=machine.Pin(19))
spi.read(100)



import machine
spi = machine.SPI(2, baudrate=40000000, polarity=1, sck=machine.Pin(18), mosi=machine.Pin(19))
spi.read(100)

import machine
spi = machine.SPI(1, baudrate=40000000, polarity=1)
spi.read(100)


from machine import SPI, Pin
import st7789
BL_Pin = 4     #backlight pin
SCLK_Pin = 18  #clock pin
MOSI_Pin = 19  #mosi pin
MISO_Pin = 2   #miso pin
RESET_Pin = 23 #reset pin
DC_Pin = 16    #data/command pin
CS_Pin = 5     #chip select pin

Pin(BL_Pin, Pin.OUT).on()


spi = SPI(baudrate=80000000, miso=Pin(MISO_Pin), mosi=Pin(MOSI_Pin, Pin.OUT), sck=Pin(SCLK_Pin, Pin.OUT))
display = st7789.ST7789(spi, 135, 240, cs=Pin(CS_Pin, Pin.OUT), dc=Pin(DC_Pin, Pin.OUT), reset=Pin(RESET_Pin, Pin.OUT))
display.init()
while True:
    display.fill(st7789.CYAN)
    display.fill(st7789.RED)


import machine
import st7789
spi = machine.SPI(2, baudrate=40000000, polarity=1)
display = st7789.ST7789(spi, 135, 240, reset=machine.Pin(4, machine.Pin.OUT), dc=machine.Pin(2, machine.Pin.OUT))
display.init()
display.fill(st7789.RED)

display.pixel(10,10,0)


spi = machine.SPI(1, baudrate=40000000, polarity=1, sck=machine.Pin(18), mosi=machine.Pin(19))
spi.read()