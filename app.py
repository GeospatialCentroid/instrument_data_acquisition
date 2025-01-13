

"""
File: add_new_instrument.py
Author: KEvin Worthington
Date: 2024-12-16
Description: The app launches a web server allowing interactivity with the InstrumentManager
The InstrumentManager looks for instruments which are transmitting data and stores these data transmissions.
Each instrument requires a configuration file and the InstrumentManager can prepopulate a template file.


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


# create data folder if it doesn't exist
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
    html="<h1>Measuring Instrument Table</h1>"
    # get the list of instruments and their latest measurement.
    # We should already have this in memory

    html += """<table>
  <tr>
    <th>Comport</th>
    <th>Instrument name</th>
    <th>Last Transmission</th>
    <th>Data</th>
  </tr>"""
    for i in instrument_manager.instruments:
        obj=instrument_manager.instruments[i]
        try:
            html +=f" <tr><td>{obj.comport}</td><td>{obj.instrument_name}</td><td>{str(obj.last_transmit)}</td><td>{obj.last_data}</td></tr>"
        except:
            pass

    html+="</table>"
    return html


@app.route("/listen_for_new")
def listen_for_new():
    instrument_manager.listen_for_new_instruments()
    return "Listening for Instruments"

@app.route("/inject_data")
def inject_data():
    print(request.args.get('comport'),">>>>>>>")
    instrument_manager.inject_data(request.args.get('comport'),request.args.get('data'))
    return "Data injected -" +request.args.get('comport')+" for:"+request.args.get('data')

@app.route("/add_new")
def add_new():
    comport = instrument_manager.add_new(request.args.get('filename'))
    return "Now watching instrument "+comport

def init():
    instrument_manager.load_configs()

if __name__ == '__main__':
    # create a single thread to maintain access to the instrument manager
    thread = threading.Thread(target=init)
    thread.start()
    app.run(host='0.0.0.0', port=5001, debug=False)


