FROM ubuntu:bionic

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq \
    && apt-get install -qqy \
    autoconf \
    automake \
    bash \
    bison \
    build-essential \
    bzip2 \
    flex \
    g++ \
    gawk \
    gcc \
    git \
    gperf \
    help2man \
    libexpat-dev \
    libffi-dev \
    libtool \
    libtool-bin \
    make \
    ncurses-dev \
    pkg-config \
    python \
    python-dev \
    python-serial \
    python3 \
    python3-pip \
    sed \
    texinfo \
    unrar-free \
    unzip \
    wget \ 
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip3 install pyparsing

RUN useradd --no-create-home micropython

RUN mkdir /esp
RUN chown -R micropython:micropython esp
USER micropython
WORKDIR /esp

# Download crosstool-NG and build it:
RUN git clone -b xtensa-1.22.x https://github.com/espressif/crosstool-NG.git
RUN cd crosstool-NG && ./bootstrap && ./configure --enable-local && make install

# Build the toolchain:
RUN cd crosstool-NG && ./ct-ng xtensa-esp32-elf
RUN cd crosstool-NG && ./ct-ng build
RUN cd crosstool-NG && chmod -R u+w builds/xtensa-esp32-elf

ARG BRANCH=master

# Find correct version of esp-idf, depends on selected branch
ADD --chown=micropython:micropython https://raw.githubusercontent.com/pfalcon/micropython/$BRANCH/ports/esp32/Makefile /tmp/ESP32-Makefile

RUN git clone https://github.com/espressif/esp-idf.git
RUN cd esp-idf && cat /tmp/ESP32-Makefile | grep "^ESPIDF_SUPHASH_V4" | awk '{print $NF}' | xargs git checkout
RUN cd esp-idf && git submodule update --init --recursive

ENV PATH="${PATH}:/esp/crosstool-NG/builds/xtensa-esp32-elf/bin"
ENV ESPIDF="/esp/esp-idf"

# Cache buster for git clone #https://stackoverflow.com/questions/36996046/how-to-prevent-dockerfile-caching-git-clone
ADD https://api.github.com/repos/pfalcon/micropython/git/refs/heads/$BRANCH version.json
RUN git clone --recursive https://github.com/pfalcon/micropython.git \
    && cd micropython && git checkout $BRANCH && git submodule update --init

RUN make --directory /esp/micropython -C mpy-cross

RUN make --directory /esp/micropython/ports/unix

# install required pyparsing version
USER root 
RUN pip3 install "pyparsing==2.3.1"
USER micropython

# add modules to be frozen in the built firmware, customize as required
RUN cd /esp/micropython/ports/unix && ./pycopy -m upip install -p ../esp32/modules \
    micropython-uasyncio \
    micropython-uaiohttpclient \
    micropython-logging

# add drivers to be frozen in the built firmware, customize as required
RUN ln /esp/micropython/drivers/display/ssd1306.py /esp/micropython/ports/esp8266/modules/ssd1306.py
RUN ln /esp/micropython/drivers/sdcard/sdcard.py /esp/micropython/ports/esp8266/modules/sdcard.py

# or download from github
RUN wget -O /esp/micropython/ports/esp32/modules/bmp280.py  https://raw.githubusercontent.com/dafvid/micropython-bmp280/master/bmp280.py

RUN git clone https://github.com/devbis/st7789_mpy.git /esp/st7789_mpy
RUN cd /esp/micropython/ports/esp32 && make USER_C_MODULES=../../../st7789_mpy/ all
# RUN cp st7789_driver/st7789 /esp/micropython/ports/esp32/modules


# # Finally build the firmware
RUN make --directory /esp/micropython/ports/esp32