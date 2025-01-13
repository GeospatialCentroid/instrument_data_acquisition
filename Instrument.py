import datetime
import os
import math
import time


class Instrument:
  def __init__(self, **config):
    self.__dict__.update(config)

  def read_from_port(self, port_obj):
    while True:
      try:
        if port_obj.in_waiting > 0:
          data = port_obj.readline().decode().strip()
          #print(f"Data from {self.instrument_name}: {data}")
          self.store_instrument_data(self.instrument_folder, self.instrument_filename,data, datetime.datetime.now(datetime.timezone.utc))
      except Exception as e:
         print(self.instrument_name,e)
    time.sleep(.25) # to save on computer resources check only every .25 of a second

  def store_instrument_data(self, instrument_folder,file_name, data, datetime):

    # first check if the data has at least once comma before continuing
    if "," not in data:
      return

    instrument_file = file_name + "_" + str(datetime.date())

    # make sure a data folder exists for the instrument
    if not os.path.exists(self.data_folder + "/" + instrument_folder):
      os.makedirs(self.data_folder + "/" + instrument_folder)

    file_path = self.data_folder + "/" + instrument_folder + "/" + instrument_file + ".csv"

    # if the file doesn't exist create it add the header
    if not os.path.exists(file_path):
      with open(file_path, "w") as f:
        f.write(self.header+"\n")

    #
    #calculate warm period based on last time
    warm_up = self.warm_up_seconds  # create a variable to output the warm_up time in seconds
    if hasattr(self, "warmup_start"):

      seconds_since_last_transmit=math.ceil((datetime - self.last_transmit).total_seconds())

      # only proceed with reducing the warm-up seconds if we have received data at an acceptable interval
      if seconds_since_last_transmit<self.interval:
        count_down_to_warm=self.warm_up_seconds - math.ceil((datetime - self.warmup_start).total_seconds())
        if count_down_to_warm>0:
          warm_up = count_down_to_warm
        else:
          warm_up=0

      else:
        # restart the warmup clock
        self.warmup_start = datetime
    else:
      self.warmup_start = datetime


    self.last_transmit = datetime

    # store the last data for easy access
    self.last_data = data

    # append (or create) data file
    with open(file_path, 'a+') as f:
      f.write(data+","+str(datetime)+","+str(warm_up)+"\n")