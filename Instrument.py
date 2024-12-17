import datetime
import os

class Instrument:
  def __init__(self, **config):
    self.__dict__.update(config)

  def read_from_port(self, port_obj):
    # while True:
      # try:
    if port_obj.in_waiting > 0:
      data = port_obj.readline().decode().strip()
      print(f"Data from {self.instrument_name}: {data}")
      self.store_instrument_data(self.instrument_folder, self.instrument_filename,data, datetime.datetime.now(datetime.timezone.utc))
      # except Exception as e:
      #   print(read_from_port,e)
  def store_instrument_data(self, instrument_folder,file_name, data, datetime):

    # first check if the data has at least once comma before continuing
    if "," not in data:
      return

    instrument_file = file_name + "_" + str(datetime.date())

    # make sure a data folder exists for the instrument
    if not os.path.exists(self.data_folder + "/" + instrument_folder):
      os.makedirs(self.data_folder + "/" + instrument_folder)

    # append (or create) data file
    with open(self.data_folder + "/" + instrument_folder + "/" + instrument_file + ".csv", 'a+') as f:
      f.write(data)