# Design

## Functional Overview

This is a very simple application, consisting of three main components:

1. **rtl\_tcp**:  rtl_tcp interfaces via USB with a Realtek RTL2832U SDR.  It is from rtl-sdr ([https://osmocom.org/projects/rtl-sdr/wiki/Rtl-sdr](https://osmocom.org/projects/rtl-sdr/wiki/Rtl-sdr))
1. **rtlamr**:  rtlamr interfaces with the SDR using rtl_tcp over a network interface using TCP.  It is by Douglas Hall, and is hosted on Github:  [https://github.com/bemasher/rtlamr](https://github.com/bemasher/rtlamr).  rtlamr outputs processed data to standard out (STDOUT). 
1. **py\_read\_rtlamr.py**:  This Python 3 program receives meter data in JSON from from rtlamr, saves the raw input to a file in the `../data` directory (`data` is at the same directory level as this application) and saves meter reading and calculated daily consumption in an SQLite data base in the `data` directory.

## Implementation Overview

Three Docker containers are used to deploy the three main components listed above.  These containers are defined in the [docker-compose.yml](../docker-compose.yml) file with service names `python`, `rtl_tcp`, and `rtlamr`.  Some implementation info that might be helpful in understanding the design:

* rtl\_tcp exposes its network interface to other containers on port 1234 (the default port used by rtl_tcp)
* rtlamr connects via TCP to rtl_tcp and programs it
* rtlamr processes the data from rtl_tcp and pipes processed JSON output to nc (netcat) which connects to the python container via TCP to port 12345 and forwards the rtlamr data.
* py_read_rtlamr.py opens a socket and waits for data to arrive from rtlamr.






