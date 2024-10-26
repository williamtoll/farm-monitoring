import serial
import datetime
import time

import logging
from pathlib import Path

logFile = Path("serial.log")


logging.basicConfig(
    filename=logFile,
    filemode="a",
    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
    level=logging.DEBUG,
)

logger = logging.getLogger("npk")
logger.setLevel(logging.DEBUG)


# Linux /dev/ttyUSB1
# Win COM#
uart0 = serial.Serial(
    port="COM29",
    # port="/dev/ttyUSB1",
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    xonxoff=False,
    rtscts =False,
    dsrdtr= False,
    timeout=1
)


start_cmd = bytes.fromhex("FF 01 85 00 00 00 00 00 7A")
status_cmd = bytes.fromhex("FF 85 31 00 00 00 00 00 4A")
change_status_cmd = bytes.fromhex("FF 01 87 32 00 00 00 00 46")
read_cmd = bytes.fromhex("FF 01 86 00 00 00 00 00 79")

result_example=bytes.fromhex("FF 86 00 5A 00 00 00 02 1E")
sensor_values = {}

def send_data(tx_cmd):
    uart0.write(tx_cmd)
    print(f"Command sent: {tx_cmd.hex().upper()}")

def send_status():
      send_data(status_cmd)

def read_data():
        data = uart0.read(9)
        print(f"Received data : {str(data)}")

        value = int.from_bytes(data[2:3], "big")
        print("command ",value)
        print("command hex",data[2:3].hex().upper())
        print(data[1:3])
        return data[2:3]

def test_data():
    print("status example")
    value = int.from_bytes(status_cmd[2:3], "big")
    print(f"Module Status: {hex(value)}")
    print("command ",value)


    print("result example")
    value = int.from_bytes(result_example[2:4], "big")
    print(f"Module Status: {hex(value)}")
    print("command ",value)


def send_result():
        send_data(result_example)



while True:
    now = datetime.datetime.now()

    #test_data()

    res =read_data()
    command_byte = int.from_bytes(res, "big")
    print(f"res: {hex(command_byte)}")
    send_status()
    if(command_byte==0x85):
      send_status()
    
    if(command_byte==0x86):
      send_result()
     
      


    time.sleep(3)
