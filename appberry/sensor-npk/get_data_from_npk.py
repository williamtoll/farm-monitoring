import serial
import datetime
import time
import geocoder


import codecs
import requests

# Initialize the geocoder
g = geocoder.ip("me")

# NPK sensor being set up
# Linux /dev/ttyUSB1
# Win COM#
uart0 = serial.Serial(
    port="COM15",
    # port="/dev/ttyUSB1",
    baudrate=4800,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1,
)


tx_command = bytes.fromhex("01 03 00 00 00 07 04 08")
sensor_values = {}


def get_sensor_values():
    if uart0.write(tx_command):
        Rx_Temp = uart0.read(19)
        print("Received data : " + str(Rx_Temp))

        value = int.from_bytes(Rx_Temp[3:5], "big")
        sensor_values["humidity"] = value/10
        print("Moisture", value)

        value = int.from_bytes(Rx_Temp[5:7], "big")
        sensor_values["temp"] = value/10
        print("Temp", value)

        value = int.from_bytes(Rx_Temp[7:9], "big")
        sensor_values["condutivity"] = value
        print("EC", value)

        value = int.from_bytes(Rx_Temp[9:11], "big")
        sensor_values["ph"] = value/10
        print("PH", value)

        value = int.from_bytes(Rx_Temp[11:13], "big")
        sensor_values["N"] = value
        print("N", value)

        value = int.from_bytes(Rx_Temp[13:15], "big")
        sensor_values["P"] = value
        print("P", value)

        value = int.from_bytes(Rx_Temp[15:17], "big")
        sensor_values["K"] = value
        print("K", value)

        value = int.from_bytes(Rx_Temp[17:19], "big")
        print("X1", value)

        return sensor_values
    else:
        print("Data Didn't Transmit")


# Get location
city = g.city

device_id = "707612a0-6d67-11ef-8156-8d12ffd8c9b3"
access_token = "lw4ryv0kosjfcwtfi4t8"
THINGSBOARD_HOST_NAME = "thingsboard.cloud"

import json
import os
import logging
from pathlib import Path

logFile = Path("npk.log")


logging.basicConfig(
    filename=logFile,
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)

logger = logging.getLogger("npk")
logger.setLevel(logging.DEBUG)


def send_to_thingboard(device, sensor_values, now):
    # curl -v -X POST http://thingsboard.cloud/api/v1/lw4ryv0kosjfcwtfi4t8/telemetry --header Content-Type:application/json --data "{temperature:25}"
    # http(s)://$THINGSBOARD_HOST_NAME/api/v1/$ACCESS_TOKEN/telemetry
    # {"ts":1451649600512, "values":{"key1":"value1", "key2":"value2"}}
    url = f"http://{THINGSBOARD_HOST_NAME}/api/v1/{access_token}/telemetry"
    ts = time.time()

    sensor_values["ts"] = ts
    sensor_values["device_id"] = device_id
    json_object = json.dumps(sensor_values, ensure_ascii=False)

    print(json.dumps(json_object, indent=4))

    logger.info("sending data to Thingboard")
    logger.info("sensor values %s ", json_object)
    headers = {"Content-type": "application/json"}

    try:
        requests.post(url, data=json_object, headers=headers)
    except requests.exceptions.HTTPError as err:
        logger.error(err)


while True:
    now = datetime.datetime.now()

    # Get the city of the current location
    sensor_values = get_sensor_values()

    send_to_thingboard(device_id, sensor_values, now)
    values = f"Timestamp: {now} \nLocation: {city} \n Device ID: {device_id}"
    # Wait for some time before checking the time again
    time.sleep(60)
