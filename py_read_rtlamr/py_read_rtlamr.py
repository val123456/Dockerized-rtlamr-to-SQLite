#!/usr/bin/env python3

import datetime
import json
import signal
import socket
import sqlite3
import time
from os import environ, fsync


# catch sigterm to gracefully shutdown when sent shutdown by docker by raising KeyboardInterrupt exception
def handle_sigterm(*args):
    raise KeyboardInterrupt()


signal.signal(signal.SIGTERM, handle_sigterm)

# function saveinput to save "raw" input for potential future reuse/reprocessing/etc
# due to potentially large number of writes, leaves file open between writes, and appends data

# open file and leave open
f = open("/data/raw_output.json", "ab+", buffering=0)


# function to save input
def saveinput(save_data):
    f.write(save_data)
    fsync(f)
    return


# function to close file
def saveinput_done():
    f.close()
    return


# function to open socket to receive rtlamr output data that is sent via netcat (nc), pass it the port


def opensocket(prt):
    print("open socket")
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Define the port on which you want to connect
    # connect to the server on local computer
    skt.bind(("", prt))
    skt.listen(1)
    connection, address = skt.accept()
    return skt, connection, address


"""
Pickup environment variables from variables.txt.
"""
# list of all meter ids to track from environment variable METERS_IDS sourced from variables.txt
meter_ids = environ["METER_IDS"].split(",")

# list of meters by type from environment variables sourced from variables.txt
electric_meter_ids = environ["ELECTRIC_METER_IDS"].split(",")
gas_meter_ids = environ["GAS_METER_IDS"].split(",")
water_meter_ids = environ["WATER_METER_IDS"].split(",")

# conversion constants to convert raw meter output to correct units
# pure luck all my meters have the same conversion
water_cnv = 100
gas_cnv = 100
electric_cnv = 100

# listening port from environment variables sourced from variables.txt
port = int(environ["PYTHON_SERVER_PORT"])

# initialize dictionary last to keep track of last meter reading to avoid saving duplicate readings
# should not happen with rtlamr settings, but just in case . . .
# updated:  can happen with R900 water meters due to use of unknown fields in my meter

last = {}
for i in meter_ids:
    last[i] = 0

# rounding constant for readings
# change to 1 or even 0 if you want to decrease number of data points
rnd = 2

# how often to checkpoint database, to minimize data loss if there is a system failure, etc
checkpoint = 5
checkpoint_count = 0

# Desired date time formats
DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S"
DATE_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M:%S"

# open SQLite database file using non-blocking journal settings so other process can read results for graphing, etc
db = sqlite3.connect("/data/meters.db")
db.execute("pragma journal_mode=wal")
con = db.cursor()

# create tables on first run, by meter ID and type.  Table Type_Meter_# for raw consumption, Table Type_DailyUse_# for calculated use upon insert.
# uses 'if not exists' for subsequents re-starts

for meter in meter_ids:

    # this is for electric meters
    if meter in electric_meter_ids:
        con.execute(
            "CREATE TABLE IF NOT EXISTS Electric_Meter_{}(id integer PRIMARY KEY, date text, time text, kWHs real, fulldatetime text)".format(
                str(meter)
            )
        )
        con.execute(
            "CREATE TABLE IF NOT EXISTS Electric_DailyUse_{}(id integer PRIMARY KEY, date text, time text, kWHs real, fulldatetime text)".format(
                str(meter)
            )
        )

        con.execute(
            "CREATE INDEX IF NOT EXISTS index_{}  ON Electric_Meter_{}(date)".format(
                str(meter), str(meter)
            )
        )
        con.execute(
            "CREATE INDEX IF NOT EXISTS index_use_{}  ON Electric_DailyUse_{}(date)".format(
                str(meter), str(meter)
            )
        )

    # gas meters
    elif meter in gas_meter_ids:
        con.execute(
            "CREATE TABLE IF NOT EXISTS Gas_Meter_{}(id integer PRIMARY KEY, date text, time text, ccf real, fulldatetime text)".format(
                str(meter)
            )
        )
        con.execute(
            "CREATE TABLE IF NOT EXISTS Gas_DailyUse_{}(id integer PRIMARY KEY, date text, time text, ccf real, fulldatetime text)".format(
                str(meter)
            )
        )

        con.execute(
            "CREATE INDEX IF NOT EXISTS index_{}  ON Gas_Meter_{}(date)".format(
                str(meter), str(meter)
            )
        )
        con.execute(
            "CREATE INDEX IF NOT EXISTS index_use_{}  ON Gas_DailyUse_{}(date)".format(
                str(meter), str(meter)
            )
        )

    # water meters
    elif meter in water_meter_ids:
        con.execute(
            "CREATE TABLE IF NOT EXISTS Water_Meter_{}(id integer PRIMARY KEY, date text, time text, cuft real, fulldatetime text)".format(
                str(meter)
            )
        )
        con.execute(
            "CREATE TABLE IF NOT EXISTS Water_DailyUse_{}(id integer PRIMARY KEY, date text, time text, cuft real, fulldatetime text)".format(
                str(meter)
            )
        )

        con.execute(
            "CREATE INDEX IF NOT EXISTS index_{}  ON Water_Meter_{}(date)".format(
                str(meter), str(meter)
            )
        )
        con.execute(
            "CREATE INDEX IF NOT EXISTS index_use_{}  ON Water_DailyUse_{}(date)".format(
                str(meter), str(meter)
            )
        )

# commit and checkpoint database
db.commit()
db.execute("pragma wal_checkpoint=FULL")

# open socket
s, conn, addr = opensocket(port)

while True:
    try:

        # 1024 grabs enough data for my meters
        # note if tracking lots of meters there is a theortical chance input will span messages.  I have not seen this in my testing
        rxdata = conn.recv(1024)
        record = {}
        use = None

        if rxdata:
            try:
                # attempt to decode JSON, catch if exception is thrown.  Have seen "invalid" JSON from rtlamr a couple of times
                raw = json.loads(rxdata)

                # save data since it is valid JSON
                saveinput(rxdata)

                # print data for logs/troubleshooting
                print("Raw ", rxdata)

                # grab meter ID from JSON
                meter = str(raw["Message"]["ID"])

                # now check by meter types based on meter type definitions in variables.txt

                # electric meter processing
                if meter in electric_meter_ids:
                    # check and see if the reading has changed.  Skip processing if not changed
                    if last[meter] != round(
                        raw["Message"]["Consumption"] / electric_cnv, rnd
                    ):
                        record["Meter"] = raw["Message"]["ID"]
                        record["DateTime"] = datetime.datetime.strptime(
                            raw["Time"].split(".", 1)[0], DATETIME_FORMAT
                        )
                        record["kWattHours"] = round(
                            raw["Message"]["Consumption"] / electric_cnv, rnd
                        )

                        data = (
                            record["DateTime"].strftime(DATE_FORMAT),
                            record["DateTime"].strftime(TIME_FORMAT),
                            record["kWattHours"],
                            record["DateTime"],
                        )

                        # pull last record in the db using current day and calculate delta daily use to make graphing easy
                        con.execute(
                            ""
                            """SELECT date, time, kWHs, fulldatetime FROM Electric_Meter_{} WHERE date is '{}' ORDER BY time ASC LIMIT 1""".format(
                                record["Meter"],
                                record["DateTime"].strftime(DATE_FORMAT),
                            )
                        )

                        use = con.fetchall()

                        if use:
                            con.execute(
                                """INSERT INTO Electric_DailyUse_{}(date, time, kWHs, fulldatetime) VALUES(?, ?, ?, ?)""".format(
                                    meter
                                ),
                                (
                                    data[0],
                                    data[1],
                                    round(data[2] - use[0][2], rnd),
                                    data[3],
                                ),
                            )
                            db.commit()
                        else:
                            con.execute(
                                """INSERT INTO Electric_DailyUse_{}(date, time, kWHs, fulldatetime) VALUES(?, ?, ?, ?)""".format(
                                    meter
                                ),
                                (data[0], "00:00:00", 0, data[0] + " 00:00:00"),
                            )

                        con.execute(
                            "INSERT INTO Electric_Meter_{}(date, time, kWHs, fulldatetime) VALUES(?, ?, ?, ?)".format(
                                meter
                            ),
                            data,
                        )

                        db.commit()

                        last[meter] = round(
                            raw["Message"]["Consumption"] / electric_cnv, rnd
                        )

                # gas meter processing
                elif meter in gas_meter_ids:
                    # check and see if the reading has changed.  Skip processing if not changed
                    if last[meter] != round(
                        raw["Message"]["Consumption"] / gas_cnv, rnd
                    ):
                        record["Meter"] = raw["Message"]["ID"]
                        record["DateTime"] = datetime.datetime.strptime(
                            raw["Time"].split(".", 1)[0], DATETIME_FORMAT
                        )
                        record["ccf"] = round(
                            raw["Message"]["Consumption"] / gas_cnv, rnd
                        )

                        data = (
                            record["DateTime"].strftime(DATE_FORMAT),
                            record["DateTime"].strftime(TIME_FORMAT),
                            record["ccf"],
                            record["DateTime"],
                        )

                        # pull last record in the db using current day and calculate delta use to make graphing easy
                        con.execute(
                            ""
                            """SELECT date, time, ccf, fulldatetime FROM Gas_Meter_{} WHERE date is '{}' ORDER BY time ASC LIMIT 1""".format(
                                record["Meter"],
                                record["DateTime"].strftime(DATE_FORMAT),
                            )
                        )

                        use = con.fetchall()

                        if use:
                            con.execute(
                                """INSERT INTO Gas_DailyUse_{}(date, time, ccf, fulldatetime) VALUES(?, ?, ?, ?)""".format(
                                    meter
                                ),
                                (data[0], data[1], (data[2] - use[0][2]), data[3]),
                            )
                            db.commit()
                        else:
                            con.execute(
                                """INSERT INTO Gas_DailyUse_{}(date, time, ccf, fulldatetime) VALUES(?, ?, ?, ?)""".format(
                                    meter
                                ),
                                (data[0], "00:00:00", 0, data[0] + " 00:00:00"),
                            )

                        con.execute(
                            "INSERT INTO Gas_Meter_{}(date, time, ccf, fulldatetime) VALUES(?, ?, ?, ?)".format(
                                meter
                            ),
                            data,
                        )

                        db.commit()

                        last[meter] = round(
                            raw["Message"]["Consumption"] / gas_cnv, rnd
                        )

                # water meter processing
                elif meter in water_meter_ids:
                    # check and see if the reading has changed.  Skip processing if not changed
                    if last[meter] != round(
                        raw["Message"]["Consumption"] / water_cnv, rnd
                    ):
                        record["Meter"] = raw["Message"]["ID"]
                        record["DateTime"] = datetime.datetime.strptime(
                            raw["Time"].split(".", 1)[0], DATETIME_FORMAT
                        )
                        record["cubicft"] = round(
                            raw["Message"]["Consumption"] / water_cnv, rnd
                        )

                        data = (
                            record["DateTime"].strftime(DATE_FORMAT),
                            record["DateTime"].strftime(TIME_FORMAT),
                            record["cubicft"],
                            record["DateTime"],
                        )

                        # pull last record in the db using current day and calculate delta use to make graphing easy
                        con.execute(
                            ""
                            """SELECT date, time, cuft, fulldatetime FROM Water_Meter_{} WHERE date is '{}' ORDER BY time ASC LIMIT 1""".format(
                                record["Meter"],
                                record["DateTime"].strftime(DATE_FORMAT),
                            )
                        )

                        use = con.fetchall()

                        if use:
                            con.execute(
                                """INSERT INTO Water_DailyUse_{}(date, time, cuft, fulldatetime) VALUES(?, ?, ?, ?)""".format(
                                    meter
                                ),
                                (
                                    data[0],
                                    data[1],
                                    round(data[2] - use[0][2], rnd),
                                    data[3],
                                ),
                            )
                            db.commit()
                        else:
                            con.execute(
                                """INSERT INTO Water_DailyUse_{}(date, time, cuft, fulldatetime) VALUES(?, ?, ?, ?)""".format(
                                    meter
                                ),
                                (data[0], "00:00:00", 0, data[0] + " 00:00:00"),
                            )

                        con.execute(
                            "INSERT INTO Water_Meter_{}(date, time, cuft, fulldatetime) VALUES(?, ?, ?, ?)".format(
                                meter
                            ),
                            data,
                        )

                        db.commit()

                        last[meter] = round(
                            raw["Message"]["Consumption"] / water_cnv, rnd
                        )

                checkpoint_count += 1
                if checkpoint_count == checkpoint:
                    db.execute("pragma wal_checkpoint=FULL")
                    db.commit()
                    print("checkpointed")
                    checkpoint_count = 0

            except json.decoder.JSONDecodeError:
                print("JSON decode error: ", rxdata)

        else:

            print("No input at {}".format(datetime.datetime.now()))
            conn.close()
            s.close()
            time.sleep(1)
            print("re-open socket")
            s, conn, addr = opensocket(port)

    except KeyboardInterrupt:
        print("Keyboard interrupt received")
        db.close()
        saveinput_done()
        conn.close()
        exit()

    # logs exception and cleanly exits to allow docker-compose settings to restart
    except Exception as e:
        print("a different exception ", e)
        db.close()
        saveinput_done()
        conn.close()
        exit()
