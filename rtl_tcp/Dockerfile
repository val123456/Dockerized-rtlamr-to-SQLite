FROM alpine:3.11

RUN apk add --no-cache \
        musl-dev \
        gcc \
        make \
        cmake \
        pkgconf \
        git \
        libusb-dev

WORKDIR /usr/local/

RUN git clone git://git.osmocom.org/rtl-sdr.git

RUN mkdir /usr/local/rtl-sdr/build
WORKDIR /usr/local/rtl-sdr/build
RUN cmake ../ -DDETACH_KERNEL_DRIVER=ON -Wno-dev
RUN make
RUN make install

WORKDIR /

EXPOSE 1234

ENTRYPOINT ["/usr/local/bin/rtl_tcp", "-a", "0.0.0.0"]
