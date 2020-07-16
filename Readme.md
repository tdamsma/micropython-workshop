## Building the firmware

Download the repository and build the Docker image:

```shell
cd micropython
docker build -t pycopy-builder .
```

This will take a while, but the image should be built after some time. After that, extract the firmware using

```shell
./get_firmware.sh pycopy-builder
```

and you should get a `firmware.bin` file in the micropython directory.

## Local python dependencies

On your local python (or in a dedicated venv) a few tools are needed to manage the firmware and python files on the esp32:

```shell
pip install adafruit-ampy rshell esptool
```

## Flash the firmware

To flash the firmware, follow these steps after the device is plugged in.

```shell
esptool.py --chip esp32 write_flash -z 0x1000 firmware.bin
```

## Interact with device

There are two tools:

- **ampy** to copy files to/from the esp32
- **rshell** to open an interactive python shell on the esp32

To prevent cluttering the command history, you can define aliases aliases with a few default parameters. Not sure what the port param should be on windows

```shell
alias amp='ampy --port /dev/ttyS5 --baud 115200'
alias rsh='rshell --port /dev/ttyS5 --baud 115200 --buffer-size 2048 repl'
```

On the ESP32 first the boot.py is run, and the main.py. Best to put custom code in main.py. To put the snake programm on the ESP32, copy main.py and display.py to the ESP32:

```shell
amp put snake/main.py main.py
amp put snake/display.py display.py
```
