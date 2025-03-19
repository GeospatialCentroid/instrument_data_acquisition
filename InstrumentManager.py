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
    self.threads = []


  def listen_for_new_instruments(self,baudrate):
    print("Listen for new instruments")
    # Watch all comports to see if one is transmitting data but not saving it
    ports = serial.tools.list_ports.comports()
    comports = []
    for port, desc, hwid in sorted(ports):
      try:
        ser = serial.Serial(port=port, baudrate=int(baudrate))#2400,19200,57600
        # check if the port already has a config
        if  port not in self.instruments:
          print("{}: {} [{}]".format(port, desc, hwid), "Could have data")
          comports.append(ser)

      except:
        pass

    # kill existing thread if it exists
    if hasattr(self, "watcher_thread"):
      try:
        self.watcher_thread.kill()
      except Exception as e:
        print("tried to kill", self.watcher_thread,e)

    # create a thread that watches for new instruments transmitting data
    self.watcher_thread = threading.Thread(target=watch_port_function, args=(self,comports))
    self.watcher_thread.daemon = True  # Make the thread a daemon so it exits when the main thread exits
    self.watcher_thread.start()

  def watch_comports(self,_comports):
    waiting=True
    while waiting:
      print("watching...")
      for i in _comports:
        # try:
        print("checking", i.port,i.in_waiting)
        if i.in_waiting > 0:
          data = i.readline()
          try:
            data = i.readline().decode("utf-8").strip()
          except Exception as e:
            pass
          current_time = datetime.datetime.now()
          print(data, current_time)
          self.create_new_instrument_config(i.port,data)
          waiting=False
        # except Exception as e:
        #   print("except",e)
        #   self.create_new_instrument_config(i.port, "")
        #   waiting = False

      time.sleep(1)

  def create_new_instrument_config(self,comport,data):
    print("create_new_instrument_config",comport,data)
    # this creates an editable config file
    config = {
      "comport": comport,  # Do not change this unless you plan on changing the comport the instrument is connected to
      "instrument_name": "",
      "instrument_filename": "",# this will be appended with _YYYY-MM-DD
      "instrument_folder": "",
      "data_folder": "data",
      "sample_line": data,
      "header": "ozone,temperature,pressure,flow,date,time,utc_datetime,warm",
      "warm_up_seconds": 600,
      "interval": 20,# When the interval is exceeded the warmup clock resets.
      "baudrate": 2400 # Adjust baudrate as needed
    }
    with open(self.config_path+"/"+comport.replace("/", "_")+'.yml', 'w') as f:
        yaml.dump(config, f, default_flow_style=False)



  def load_configs(self):
    # look through the config folder and load all yaml files
    for filename in os.listdir(self.config_path):
      file_path = os.path.join(self.config_path, filename)

      if os.path.isfile(file_path) and file_path.endswith(".yml"):
        self.open_config(file_path)

    self.watch_instruments()

  def add_new(self, filename):
    # Allow a new instrument to be watched while the application is running without disrupting other threads
    comport = self.open_config(self.config_path + "/" + filename)
    self.create_instrument_thread(comport)
    return comport

  def open_config(self, file_path):
    with open(file_path, 'r') as file:
      instrument_config = yaml.safe_load(file)
      print(instrument_config)
      # add dictionary item referring to instrument comport
      self.instruments[instrument_config['comport']] = Instrument.Instrument(**instrument_config)
      return instrument_config['comport']

  def watch_instruments(self):
    print("WATCH >>>", self.instruments)

    for i in self.instruments:
      self.create_instrument_thread(i)

    # Keep the main thread alive
    while True:
      time.sleep(1)

  def create_instrument_thread(self,comport):
    # use 'obj' to more easily access each instrument object
    obj = self.instruments[comport]
    try:
      port_obj = serial.Serial(obj.comport, obj.baudrate)  #
      thread = threading.Thread(target=read_from_port_function, args=(obj, port_obj))
      thread.daemon = True
      thread.start()
      self.threads.append(thread)
    except serial.SerialException:
      print(f"Error: Could not open port {comport}")

  def inject_data(self,comport, data):
    #for testing the app
    print(self.instruments)
    obj = self.instruments[comport]
    obj.store_instrument_data(obj.instrument_folder, obj.instrument_filename, data,
                               datetime.datetime.now(datetime.timezone.utc))


def read_from_port_function(obj, _port_obj):
  # new thread function created for each instrument
  obj.read_from_port(_port_obj)

def watch_port_function(obj, _comports):
  # single thread to watch for comports when adding a new instrument
  obj.watch_comports(_comports)





