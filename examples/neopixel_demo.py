import time
import machine, neopixel


def demo(np):
    n = np.n

    # cycle
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 0)
        np[i % n] = (255, 255, 255)
        np.write()
        time.sleep_ms(25)

    # bounce
    for i in range(4 * n):
        for j in range(n):
            np[j] = (0, 0, 128)
        if (i // n) % 2 == 0:
            np[i % n] = (0, 0, 0)
        else:
            np[n - 1 - (i % n)] = (0, 0, 0)
        np.write()
        time.sleep_ms(60)

    # fade in/out
    for i in range(0, 4 * 256, 8):
        for j in range(n):
            if (i // 256) % 2 == 0:
                val = i & 0xFF
            else:
                val = 255 - (i & 0xFF)
            np[j] = (val, 0, 0)
        np.write()

    # clear
    for i in range(n):
        np[i] = (0, 0, 0)
    np.write()


np = neopixel.NeoPixel(machine.Pin(15), 12)
demo(np)

n = np.n

while True:
    for p in range(160):
        for i in range(n):
            k = int(abs(((p / 10) ** 2 * 2) - 255))
            np[i] = (k, k + 100 * i, k + 200 * i)
        np.write()
        time.sleep(0.01)

    for k in range(12):
        for n in range(12):
            i = (n + k) % 12
            np[n] = [0, 0, i ** 2]
        np.write()
        time.sleep(0.1)
