from machine import SPI, Pin, SoftSPI
from sysfont import sysfont
from st7789 import ST7789, WHITE, BLACK, color565, map_bitarray_to_rgb565

w = sysfont["Width"]
h = sysfont["Height"]
start = sysfont["Start"]
data = sysfont["Data"]
buffer = bytearray(w * h * 2)


class Display(ST7789):
    def draw_letter(self, x, y, c, color=WHITE, bg_color=BLACK):
        i = ord(c) - start
        map_bitarray_to_rgb565(
            data[i * 5 : (i + 1) * 5], buffer, h, color=color, bg_color=bg_color,
        )
        self.blit_buffer(
            buffer, x, y, h, w,
        )

    def draw_text(self, x, y, text, spacing=1, color=WHITE, bg_color=BLACK):
        for letter in text:
            self.draw_letter(x, y, letter, color=color, bg_color=bg_color)
            y += w
            self.fill_rect(x, y, h, spacing, bg_color)
            y += 1


BL_Pin = 4  # backlight pin
SCLK_Pin = 18  # clock pin
MOSI_Pin = 19  # mosi pin
MISO_Pin = 2  # miso pin
RESET_Pin = 23  # reset pin
DC_Pin = 16  # data/command pin
CS_Pin = 5  # chip select pin

Pin(BL_Pin, Pin.OUT).on()

spi = SoftSPI(
    baudrate=80_000_000,
    miso=Pin(MISO_Pin),
    mosi=Pin(MOSI_Pin, Pin.OUT),
    sck=Pin(SCLK_Pin, Pin.OUT),
)

display = Display(
    spi,
    135,
    240,
    cs=Pin(CS_Pin, Pin.OUT),
    dc=Pin(DC_Pin, Pin.OUT),
    reset=Pin(RESET_Pin, Pin.OUT),
)


display.init()
