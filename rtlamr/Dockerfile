FROM alpine:3.11

RUN apk add --no-cache \
        go \
        git \
        bash \
        gcc \
        binutils \
        musl-dev \
        netcat-openbsd 

RUN go get -v github.com/bemasher/rtlamr

ENV TZ=America/New_York

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ADD script.sh /

# CMD ["bash", "script.sh"]

ENTRYPOINT ["/bin/bash", "script.sh"]
