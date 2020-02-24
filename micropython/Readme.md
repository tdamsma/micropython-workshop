docker build -t pycopy .
docker create --name pycopy pycopy
docker cp pycopy:/esp/micropython/ports/esp32/build-GENERIC/firmware.bin firmware.bin
docker rm pycopy

docker run --rm -it pycopy bash

esptool.py --port /dev/ttyS5 --chip esp32 erase_flash
esptool.py --chip esp32 erase_flash
esptool.py --chip esp32 write_flash -z 0x1000 firmware.bin

alias amp='ampy --port /dev/ttyS5 --baud 115200'
alias rsh='rshell --port /dev/ttyS5 --baud 115200 --buffer-size 2048 repl'

pip install adafruit-ampy rshell esptool
