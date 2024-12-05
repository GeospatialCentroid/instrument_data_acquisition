import serial
import serial.tools.list_ports

import time

import datetime



ports = serial.tools.list_ports.comports()
working_serials=[]
for port, desc, hwid in sorted(ports):
    print("checking ",port)
    try:
        ser = serial.Serial(port=port, baudrate=2400)
        print("{}: {} [{}]".format(port, desc, hwid), "works")
        working_serials.append(ser)
    except:
        pass
print ("watching",working_serials)
while True:
    for i in working_serials:
        if i.in_waiting>0:
            value=i.readline().decode("utf-8").strip()
            current_time = datetime.datetime.now()
            print(i.port)

            print(value,current_time)

    time.sleep(1)