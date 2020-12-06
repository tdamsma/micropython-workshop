from display import display
from machine import Pin
from st7789 import BLUE, GREEN, RED, YELLOW, CYAN, MAGENTA, color565
from time import sleep
import utime
import random
from array import array

TICK_DURATION_MS = 200
BLOCK_SIZE = 20
HEIGHT = 135 // BLOCK_SIZE
WIDTH = 240 // BLOCK_SIZE

global TURN


def handle_button_input():

    Button1_Pin = 35  # right button
    Button2_Pin = 0  # left button
    button1 = Pin(Button1_Pin, Pin.IN, Pin.PULL_UP)
    button2 = Pin(Button2_Pin, Pin.IN, Pin.PULL_UP)

    def callback_b1(p):
        global TURN
        TURN = "turn_left"

    def callback_b2(p):
        global TURN
        TURN = "turn_right"

    button1.irq(
        trigger=Pin.IRQ_RISING, handler=callback_b1
    )  # interrupt for right button (button 2)
    button2.irq(
        trigger=Pin.IRQ_RISING, handler=callback_b2
    )  # interrupt for left button (button 1)


def init(display):
    global TURN
    TURN = None

    board = array("b", [0] * HEIGHT * WIDTH)
    pos_x = HEIGHT // 2
    pos_y = WIDTH // 2
    length = 3
    display.fill(0)
    length = 3
    dir = "up"
    set_goal(board)

    return (pos_x, pos_y, length, dir, board)


def turn_left(dir):
    return {"up": "left", "left": "down", "down": "right", "right": "up",}[dir]


def turn_right(dir):
    return {"left": "up", "down": "left", "right": "down", "up": "right",}[dir]


def dir_to_dxdy(dir):
    return {"left": (-1, 0), "down": (0, -1), "right": (1, 0), "up": (0, 1)}[dir]


def xy_to_i(x, y):
    return (x * WIDTH) + y


def i_to_xy(i):
    x = i // WIDTH
    y = i - (WIDTH * x)
    return x, y


def paint_xy(x, y, color):
    display.fill_rect(
        x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE - 1, BLOCK_SIZE - 1, color,
    )


def paint_i(i, color):
    x, y = i_to_xy(i)
    paint_xy(x, y, YELLOW)


def set_goal(board):
    while True:
        goal = random.randint(0, (HEIGHT * WIDTH) - 1)
        if board[goal] == 0:
            break
    board[goal] = -1
    paint_i(goal, YELLOW)


if __name__ == "__main__":
    global TURN
    handle_button_input()
    pos_x, pos_y, length, dir, board = init(display)

    print("starting game")
    # main loop
    while True:
        # clear board / decrement snake counts
        for i, v in enumerate(board):
            if v > 0:
                board[i] = v - 1
                x, y = i_to_xy(i)
                if v == 1:
                    color = 0
                else:  # snake is green/cyan
                    if v % 3:
                        color = CYAN
                    else:
                        color = GREEN
                paint_xy(x, y, color)

        # determine next position with wrap around
        if TURN == "turn_left":
            dir = turn_left(dir)
        elif TURN == "turn_right":
            dir = turn_right(dir)
        TURN = None
        dx, dy = dir_to_dxdy(dir)
        pos_x += dx
        pos_y += dy

        if pos_x == HEIGHT:
            pos_x = 0
        elif pos_x == -1:
            pos_x = HEIGHT - 1
        if pos_y == WIDTH:
            pos_y = 0
        elif pos_y == -1:
            pos_y = WIDTH - 1

        i = xy_to_i(pos_x, pos_y)

        if board[i] > 0:
            # game over...
            # reset
            display.fill(RED)
            display.fill(BLUE)
            display.fill(GREEN)
            pos_x, pos_y, length, dir, board = init(display)
            continue

        elif board[i] == -1:
            # goal hit
            length += 1
            set_goal(board)

        board[i] = length
        paint_xy(pos_x, pos_y, RED)
        utime.sleep_ms(TICK_DURATION_MS)

