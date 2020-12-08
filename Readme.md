# Micropython on an ESP32

This is a workshop for using micropython on a ttgo ESP32 with integrated 240 x 135 pixel lcd color display

<img src="https://imgaz3.staticbg.com/thumb/large/oaupload/banggood/images/16/CA/808b45ee-f288-4048-a4a9-b21a5d1c7e13.jpg" alt="ESP32"
	title="ESP32 with display" width="50%" height="50%" />


## Preparations

Install drivers for the USB to UART Bridge
Find them here: https://www.silabs.com/developers/usb-to-uart-bridge-vcp-drivers
This one for windows: https://www.silabs.com/documents/public/software/CP210x_Universal_Windows_Driver.zip

in python on (and if on windows (not WSL)
pip install esptool, rshell, adafruit-ampy

esptool --chip esp32 chip_id



git clone git@github.com:tdamsma/micropython-workshop.git
python -m virtualenv --prompt mpy .venv



AMPY_PORT = COM6
RSHELL_PORT = COM6

https://github.com/dhylands/rshell

--buffer-size


rshell -p COM6 repl
## Building the firmware

To run the latest version of the pycopy micropython fork with driver for the display follow the steps below:

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

On the ESP32 first the boot.py is run, and the main.py. Best to put custom code in main.py. 

## Snake demo

To put the snake program on the ESP32, copy main.py and display.py to the ESP32:

```shell
amp put snake/main.py main.py
amp put snake/display.py display.py
```
Now reboot (powercycle, press reset butto on right, or hit ctrl+D in rshell python interpreter) and the snake game starts
