esptool --chip esp32 erase_flash
esptool --chip esp32 write_flash -z 0x1000 micropython/firmware.bin