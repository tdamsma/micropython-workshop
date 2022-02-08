To build a custom pycopy/micropython this dockerfile can be used and adapted for your needs

```
IMAGE_NAME=pycopy
docker build -t $IMAGE_NAME .
SRC_FIRMWARE=/home/esp32/micropython/ports/esp32/build-GENERIC/firmware.bin
DST_FIRMWARE=firmware.bin
docker create -ti --name dummy $IMAGE_NAME bash 1>/dev/null
docker cp dummy:$SRC_FIRMWARE $DST_FIRMWARE
docker rm -f dummy 1>/dev/null
```

## Flashing custom firmware

```
esptool.py --chip esp32 erase_flash
esptool.py --chip esp32 write_flash -z 0x1000 firmware.bin
```
