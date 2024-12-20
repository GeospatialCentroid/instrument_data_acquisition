# Instrument Data Acquisition System

This application is used for capturing data transmitted from instruments connected through serial ports.
Many instruments can be connected, and all transmitted data is stored as daily csv files using UTC dates and time.

## Installation
This program uses Python 3.x. and is best managed using a virtual environment. Please first install Python, then to create the virtual environment, from the terminal, execute:
Note: Be sure to have your terminal path set to the cloned git repository

```python3 -m venv venv
source venv/bin/activate
```
Then to load the required python libraries into the virtual environment use:
```
pip install -r requirements.txt 
```
or to skip errors
```
cat requirements.txt | xargs -n 1 pip install
```

## Running the program
With the virtual environment activated, run:
```
python app.py
```

## Interactions
This application can be interacted with from either your web browser, or using the terminal (prefacing each URL with 'curl')


### Create a new instrument configuration
For this program to be useful, you first need to add instruments to be 'watched'.
With a new instrument connected, and running, go to http://127.0.0.1:5001/listen_for_new.
This will trigger the program to look for any instruments that are transmitting data but not yet being 'watched'.
When the new instrument first starts transmitting, a config file is created.

#### Config files
All the properties for each instrument are stored in .yml files.
While these files can be created manually, it's best to have the program first prepopulate the template file which you should then edit.
These prepopulated template files are named using the serial port, but can be named whatever you like, so long as the '.yml' extension is retained.

##### Editing Config files
.yml files should be edited using a basic text editor.

The .yml files have been designed for readability but formatting is still strict.

Each line is a new 'key: value' pair.

Be sure there's a space after the ':' to avoid errors

##### Add new configuration
With the new instrument configuration file updated, go to http://127.0.0.1:5001/add_new?filename={filename}, replacing '{filename}' with the name of the file in the config folder.

## Get Latest Instrument Measurements
While the app is running, go to http://127.0.0.1:5001/ to see a table of instruments being 'watched' and their last transmission

## Testing
Once you have a config file, you can test how data is saved using the following:
http://127.0.0.1:5001/inject_data?comport=/dev/cu.Bluetooth-Incoming-Port&data=12.0,26.5,826.6,1836,05/12/24,16:01:392024-12-0516:01:16.699350



