

"""
File: add_new_instrument.py
Author: KEvin Worthington
Date: 2024-12-16
Description: The app is launched a web server is started allowing interactivity with the InstrumentManager


Run with
```
python app.py
```

"""


from flask import Flask, request
import threading
import os
import InstrumentManager

app = Flask(__name__)


# create data folder if it doesn't exists
data_folder= "data"
if not os.path.exists(data_folder):
   os.makedirs(data_folder)

config_folder= "config"
if not os.path.exists(config_folder):
   os.makedirs(config_folder)

instrument_manager = InstrumentManager.InstrumentManager(data_folder=data_folder, config_folder=config_folder)


@app.route("/")
def root():
    print("Preparing measurement table")
    html="Measuring Instrument Table"
    # get the list of instruments and their latest measurement.
    # We should already have this in memory

    return html


@app.route("/add_new")
def add_new():
    instrument_manager.listen_for_instrument()
    return "Listening for Instruments"

@app.route("/inject_data")
def inject_data():
    print(request.args.get('comport'),">>>>>>>")
    instrument_manager.inject_data(request.args.get('comport'),request.args.get('data'))
    return "Data injected"

@app.route("/reload_configs")
def reload_configs():
    # todo when a change is made to a config file
    # restarting app will reload the configs
    return "reload_configs..."

def init():
    instrument_manager.load_configs()

if __name__ == '__main__':

    thread = threading.Thread(target=init)
    thread.start()
    app.run(host='0.0.0.0', port=5001, debug=False)


