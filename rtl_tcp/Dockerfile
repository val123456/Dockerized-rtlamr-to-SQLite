FROM alpine:3.11

# add packages needed to compile and run rtl_tcp 
# see https://osmocom.org/projects/rtl-sdr/wiki/Rtl-sdr#Building-the-software

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

# allow other containers to access rtl_tcp's default port
EXPOSE 1234

ENTRYPOINT ["/usr/local/bin/rtl_tcp", "-a", "0.0.0.0"]
