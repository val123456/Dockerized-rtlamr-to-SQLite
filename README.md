# Acknowledgments  

This project leverages the great work done by Douglas Hall ([https://github.com/bemasher](https://github.com/bemasher)) on rtlamr, a rtl-sdr receiver for Itron ERT compatible smart meters operating in the 900MHz ISM band.  Project link for rtlamr:  [https://github.com/bemasher/rtlamr](https://github.com/bemasher/rtlamr).  He has also some work with Docker (see [https://hub.docker.com/u/bemasher](https://hub.docker.com/u/bemasher)).

# Background

I've been using rtlamr plus some custom collection and graphing code on my general purpose Linux server for several years to track electric usage and solar panel output.  In the middle of 2019 I decided to move it to a [Raspberry Pi](https://www.raspberrypi.org/).  At that time I decided to see if using [Docker](https://www.docker.com/) and [Docker Compose](https://docs.docker.com/compose/) could help with managing deployment and fault tolerance.

So far the results are very promising, and I have decided to open source the result.  Docker-ized RTLAMR Meter Scanner was the first release, designed to help potential users test rtlamr and see if their meter data can be collected ([https://gitlab.com/colinv/docker-rtlamr-meter-scanner](https://gitlab.com/colinv/docker-rtlamr-meter-scanner)). 

This project, Docker-ized rtlamr to SQLite is the second release.  It reads the JSON output from rtlamr and puts the meter reading and calculated running current daily use in SQLite tables.  

Storing the data in SQLite form allows for many uses.  The graph shown here [https://val123456.github.io/index.html](https://val123456.github.io/index.html) was generated with [Plotly](https://plot.ly/) and allows zooming, etc.  My third release will be the code used to generate graphs from the SQLite database.

# Requirements 

Linux OS with Docker and Docker Compose installed and an RTL2832U SDR.  I have had good luck with the dongles from RTL-SDR ([https://www.rtl-sdr.com/buy-rtl-sdr-dvb-t-dongles/](https://www.rtl-sdr.com/buy-rtl-sdr-dvb-t-dongles/)).

This project has been tested on the following using my SCM electric and gas meters and R900 water meter:



| OS  | Docker | Docker Compose |Hardware| 
| ------------- | ------------- |------------|---------|
| CentOS 7.7 (x86_64)|19.03.5|1.18.0|Dell PowerEdge T20|
|Ubuntu 18.04.3 LTS (aarch64)|18.09.7|1.17.1|Raspberry Pi 3 B+|
|Raspbian 10 (buster)|19.03.5|1.25.0|Raspberry Pi 4 B|


**Note**: This will not work on Mac OS X due to the way the USB is handled when using Docker.  I will release a version that works on Mac "soon".

# Building/Using
Download/clone source.  Open a terminal, `cd` into the top-level directory and run `docker-compose build` to build the container.  

Edit the text file `variables.txt` to include your meter ids.  It will work with gas, water, or electric meters.  See more info by reading the file and [docs/variables](docs/variables.md).

Then run `docker-compose up -d` to run it.  Output is placed in a directory called `data` at the same level (e. g., `../data/`.  To stop, use `docker-compose down`.

**Note:** On some systems, you may have to run these as commands as root using sudo: `sudo docker-compose build` and `sudo docker-compose up -d`


On most systems you can avoid using `sudo` by adding your account to the docker group like this:

`sudo gpasswd -a $USER docker`

## Expected Output

The data directory will look like this while the program is running.  `raw_output.json` is the raw output from rtlamr that is saved in case you want to re-process the data at some point in the future (application for that will be released in the future after it is documented).


```bash
pi@pi4:~/development/data $ ls -lh
total 13M
-rw-r--r-- 1 pi pi 5.8M Jan 25 11:31 meters.db
-rw-r--r-- 1 pi pi  32K Jan 25 11:31 meters.db-shm
-rw-r--r-- 1 pi pi    0 Jan 25 11:31 meters.db-wal
-rw-r--r-- 1 pi pi 6.6M Jan 25 11:31 raw_output.json
```

Data is stored in SQLite.  The schema in SQL form is contained in [docs/schema](docs/schema.md).  Note the meter IDs are used in the table names.  The documentation here shows my meter IDs.
 