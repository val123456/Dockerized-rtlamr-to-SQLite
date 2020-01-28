FROM python:3-slim

RUN mkdir /data

ENV TZ=America/New_York

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

EXPOSE 12345

ADD py_read_rtlamr.py /

CMD [ "python", "-u", "./py_read_rtlamr.py" ]
