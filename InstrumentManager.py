import os
import yaml

import Instrument

import serial
import serial.tools.list_ports
import threading
import time

import datetime

class InstrumentManager:
  def __init__(self, data_folder, config_folder):
    self.data_path = data_folder
    self.config_path = config_folder
    # track the instruments
    self.instruments={}


  def listen_for_instrument(self):
    print("Listen for instrument")
    # Watch all comports to see if one is transmitting data but not saving it
    # When a new comport is seen, create a new config file
    ports = serial.tools.list_ports.comports()
    comports = []
    for port, desc, hwid in sorted(ports):
      print("checking ", port)
      try:
        ser = serial.Serial(port=port, baudrate=2400)
        print("{}: {} [{}]".format(port, desc, hwid), "works")
        comports.append(ser)
      except:
        pass
    self.watch_comports(comports)

  def watch_comports(self,_comports):
    print("watching", _comports)
    while True:
      for i in _comports:
        try:
          if i.in_waiting > 0:
            data = i.readline().decode("utf-8").strip()
            current_time = datetime.datetime.now()
            print(i.port)

            print(data, current_time)
            self.create_new_instrument_config(i.port,data)
        except Exception as e:
          print("except",e)
          self.create_new_instrument_config(i.port, "")

      time.sleep(1)

  def create_new_instrument_config(self,comport,data):
    # this creates an editable config file
    config = {
      "comport": comport,  # Do not change this unless you plan on changing the comport the instrument is connected to
      "instrument_name": "",
      "instrument_filename": "",# this will be appended with _YYYY-MM-DD
      "instrument_folder": "",
      "data_folder": "data",
      "sample_line": data,
      "header": "ozone,temperature,pressure,flow,date,time,warm",
      "warm-up_seconds": "",
      "baudrate": 2400 # Adjust baudrate as needed
    }
    with open(self.config_path+"/"+comport.replace("/", "_")+'.yml', 'w') as f:
        yaml.dump(config, f, default_flow_style=False)

  def load_configs(self):
    # look through the config folder and load all yaml files
    for filename in os.listdir(self.config_path):
      file_path = os.path.join(self.config_path, filename)

      if os.path.isfile(file_path):
        with open(file_path, 'r') as file:
          instrument_config=yaml.safe_load(file)
          # create an instrument for each config file, and make it accessible by the comport value
          print(instrument_config)
          self.instruments[instrument_config['comport']]=Instrument.Instrument(**instrument_config)

    self.watch_instruments()

  def watch_instruments(self):
    print("WATCH >>>", self.instruments)
    threads=[]
    for i in self.instruments:
      # use 'obj' to more easily access each instrument object
      obj=self.instruments[i]
      try:
        port_obj = serial.Serial(obj.comport, obj.baudrate, timeout=1)  #
        thread = threading.Thread(target=worker_function, args=(obj,port_obj))
        thread.daemon = True
        thread.start()
        threads.append(thread)
      except serial.SerialException:
        print(f"Error: Could not open port {port_name}")

    # Keep the main thread alive
    while True:
      time.sleep(1)

  def inject_data(self,comport, data):
    #for testing the app
    print(self.instruments)
    obj = self.instruments[comport]
    obj.store_instrument_data(obj.instrument_folder, obj.instrument_filename, data,
                               datetime.datetime.now(datetime.timezone.utc))


def worker_function(obj, arg1):
  obj.read_from_port(arg1)





