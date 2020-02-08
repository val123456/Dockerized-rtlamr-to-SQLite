# Monitoring

There are several ways to monitor this application.

## Monitoring via Docker

Run `docker ps` in a terminal window.  Output should look like this:

```bash
pi@pi4:~/development/gitlab/docker-ized-rtlamr-to-sqlite $ docker ps
CONTAINER ID        IMAGE                                  COMMAND                  CREATED             STATUS              PORTS               NAMES
f699a2275039        docker-ized-rtlamr-to-sqlite_python    "python -u ./py_read…"   10 hours ago        Up 10 hours         12345/tcp           docker-ized-rtlamr-to-sqlite_python_1
022db96ccb31        docker-ized-rtlamr-to-sqlite_rtlamr    "/bin/bash script.sh"    10 hours ago        Up 10 hours                             docker-ized-rtlamr-to-sqlite_rtlamr_1
ea1785c687c4        docker-ized-rtlamr-to-sqlite_rtl_tcp   "/usr/local/bin/rtl_…"   10 hours ago        Up 10 hours         1234/tcp            docker-ized-rtlamr-to-sqlite_rtl_tcp_1
```

Run `docker stats` in a terminal window.  Type `CTRL-c` to exit.  It should look like this:

```bash
CONTAINER ID        NAME                                     CPU %               MEM USAGE / LIMIT     MEM %               NET I/O             BLOCK I/O           PIDS
f699a2275039        docker-ized-rtlamr-to-sqlite_python_1    0.00%               5.801MiB / 3.814GiB   0.15%               406kB / 66.1kB      16.4kB / 20.3MB     1
022db96ccb31        docker-ized-rtlamr-to-sqlite_rtlamr_1    76.35%              8.074MiB / 3.814GiB   0.21%               165GB / 102MB       4.1kB / 0B          15
ea1785c687c4        docker-ized-rtlamr-to-sqlite_rtl_tcp_1   3.74%               4.676MiB / 3.814GiB   0.12%               103MB / 165GB       0B / 0B             4
```

Run `docker-compose logs` in the top level directory of this application.  Logs should be dumped to the screen like this:

```bash
python_1   | Raw  {'Time': '2020-02-08T07:42:58.683909147-05:00', 'Offset': 0, 'Length': 0, 'Type': 'SCM', 'Message': {'ID': 629848, 'Type': 5, 'TamperPhy': 0, 'TamperEnc': 1, 'Consumption': 2783622, 'ChecksumVal': 4549}}
python_1   | checkpointed
python_1   | Raw  {'Time': '2020-02-08T07:48:00.695326149-05:00', 'Offset': 0, 'Length': 0, 'Type': 'SCM', 'Message': {'ID': 629848, 'Type': 5, 'TamperPhy': 0, 'TamperEnc': 1, 'Consumption': 2783623, 'ChecksumVal': 62247}}
python_1   | Raw  {'Time': '2020-02-08T07:49:35.689688159-05:00', 'Offset': 0, 'Length': 0, 'Type': 'SCM', 'Message': {'ID': 44448439, 'Type': 12, 'TamperPhy': 0, 'TamperEnc': 0, 'Consumption': 436034, 'ChecksumVal': 16435}}
python_1   | Raw  {'Time': '2020-02-08T07:51:36.220453288-05:00', 'Offset': 0, 'Length': 0, 'Type': 'SCM', 'Message': {'ID': 44448439, 'Type': 12, 'TamperPhy': 0, 'TamperEnc': 0, 'Consumption': 436038, 'ChecksumVal': 31262}}
python_1   | Raw  {'Time': '2020-02-08T07:52:35.690654262-05:00', 'Offset': 0, 'Length': 0, 'Type': 'SCM', 'Message': {'ID': 44448439, 'Type': 12, 'TamperPhy': 0, 'TamperEnc': 0, 'Consumption': 436040, 'ChecksumVal': 40654}}
python_1   | Raw  {'Time': '2020-02-08T07:53:34.046428486-05:00', 'Offset': 0, 'Length': 0, 'Type': 'SCM', 'Message': {'ID': 629848, 'Type': 5, 'TamperPhy': 0, 'TamperEnc': 1, 'Consumption': 2783624, 'ChecksumVal': 62741}}
python_1   | checkpointed
python_1   | Raw  {'Time': '2020-02-08T07:53:50.692982998-05:00', 'Offset': 0, 'Length': 0, 'Type': 'SCM', 'Message': {'ID': 44448439, 'Type': 12, 'TamperPhy': 0, 'TamperEnc': 0, 'Consumption': 436042, 'ChecksumVal': 13417}}
```

Run `docker-compose logs -f` in the top level directory of this application to follow the logs.  

**Note** some versions of docker-compose will eventually hang if you follow the logs for a long time.

## Monitoring the Output

From the top level directory of this application look at the saved raw input by running `less ../data/raw_output.json`.  Output should look like this:

```bash
{"Time":"2020-02-07T22:09:05.470325791-05:00","Offset":0,"Length":0,"Type":"SCM","Message":{"ID":44448439,"Type":12,"TamperPhy":0,"TamperEnc":0,"Consumption":435760,"ChecksumVal":57994}}
{"Time":"2020-02-07T22:09:07.905250319-05:00","Offset":0,"Length":0,"Type":"SCM","Message":{"ID":629848,"Type":5,"TamperPhy":0,"TamperEnc":1,"Consumption":2783390,"ChecksumVal":49407}}
{"Time":"2020-02-07T22:09:28.963747635-05:00","Offset":0,"Length":0,"Type":"SCM","Message":{"ID":22277181,"Type":7,"TamperPhy":1,"TamperEnc":0,"Consumption":7329333,"ChecksumVal":63807}}
{"Time":"2020-02-07T22:09:37.634567567-05:00","Offset":0,"Length":0,"Type":"R900","Message":{"ID":1563476986,"Unkn1":163,"NoUse":32,"BackFlow":0,"Consumption":111051,"Unkn3":0,"Leak":1,"LeakNow":0}}
{"Time":"2020-02-07T22:09:38.589477618-05:00","Offset":0,"Length":0,"Type":"SCM","Message":{"ID":629848,"Type":5,"TamperPhy":0,"TamperEnc":1,"Consumption":2783391,"ChecksumVal":8733}}
{"Time":"2020-02-07T22:11:05.513266601-05:00","Offset":0,"Length":0,"Type":"SCM","Message":{"ID":44448439,"Type":12,"TamperPhy":0,"TamperEnc":0,"Consumption":435762,"ChecksumVal":18477}}
{"Time":"2020-02-07T22:11:29.845223818-05:00","Offset":0,"Length":0,"Type":"SCM","Message":{"ID":22277181,"Type":7,"TamperPhy":1,"TamperEnc":0,"Consumption":7329338,"ChecksumVal":65293}}
```

You can follow the raw input by running `less +F ../data/raw_output.json`.

You can make sure the database and raw inputs are being updated by looking at the file modified times.  From the top level directory of this application run `ls -lh ../data/`.  Output should look like this:

```bash
total 19M
-rw-r--r-- 1 val val 8.5M Feb  8 08:00 meters.db
-rw-r--r-- 1 val val  32K Feb  8 08:03 meters.db-shm
-rw-r--r-- 1 val val  50K Feb  8 08:03 meters.db-wal
-rw-rw-r-- 1 val val  11M Feb  8 08:03 raw_output.json
```
Note this data set has 39 days of data with 4 meters (two electric, one water, and one gas).  `meters.db` time will be updated after every checkpoint (after every 5 additions).




