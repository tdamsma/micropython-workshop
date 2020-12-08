setx AMPY_PORT COM6
setx RSHELL_PORT COM6
ampy put library/display.py
ampy put library/sysfont.py

RSHELL_PORTCOM6
ampy -p COM6 put snake.py main.py
rshell -p COM6 repl