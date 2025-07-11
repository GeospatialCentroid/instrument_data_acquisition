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
With a new instrument connected, and running, go to http://127.0.0.1:5001/listen_for_new?baudrate=2400
Replacing the baud rate number (2400) to whatever your new instrument uses.

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

Note: Be sure there's a space after the ':' to avoid errors

#### Config File options
* comport: The name of the comport the instrument is connected to. Do not change this unless you plan on changing the comport the instrument is connected to
* instrument_name: The name of the instrument for use on web pages and print statements
* instrument_filename: The prefix you'd like added to each of your files. this will be appended with _YYYY-MM-DD
* instrument_folder: The name of the folder for the instrument data
* data_folder: The folder for all the instrument's. Best to leave this as "data"
* sample_line: When an instrument is first noticed to be transmitting data, this sample data line will appear here
* header: When a new data file is created, this header line is added. Each line of data is also appended with a "utc_datetime", and "warm" value
  * utc_datetime or Universal Time Coordinated (UTC), is equivalent to the time at the Greenwich Meridian in London, England, without adjustment for daylight savings
* warm_up_seconds: The number of seconds it take for the instrument to warm up. This number is subtracted from using the time data is transmitted
* interval: When the interval number is exceeded between data transmissions, the warmup clock resets
* baudrate: Determined by the instrument manufacturer. Adjust based on instrument manual.

##### Add new configuration
With the new instrument configuration file updated, and while the app is still running, go to http://127.0.0.1:5001/add_new?filename={filename}, replacing '{filename}' with the name of the file in the config folder.

## Get Latest Instrument Measurements
While the app is running, go to http://127.0.0.1:5001/ to see a table of instruments being 'watched' and their last transmission

## Testing
Once you have a config file, you can test how data is saved using the following:
http://127.0.0.1:5001/inject_data?comport={comport}&data=12.0,26.5,826.6,1836,05/12/24,16:01:392024-12-0516:01:16.699350, replacing '{comport}' with the name of the comport you are testing



## Accessing file on a remote computer over SSH
1. Open the terminal - if you're using NinjaOne - navigate to https://csuspur.rmmservice.com/eus/#/devices and click the >_ icon
   1. Otherwise: To SSH into the computer enter the {remote computer user}@{IP address}
1. Change the directory to where your files are located ```cd {file location dir}```
1. type ```nano {name of file}``` to open or use ```tail -f {name of file}``` to see real-time updates to a file.


## Storing data on a mounted drive
To allow the data to be stored on a separate drive (preferably one that is set up using RAID),
be sure the mounted drive is added to the ```fstab``` listing to ensure it gets remounted when the computer reboots.
The steps to update ```fstab``` are:
1. run ```lsblk -f``` and take note of the UUID for the mounted drive
1. run  ```sudo nano /etc/fstab```
1. add ```UUID=5fcfba13-288b-4c55-a215-19ae047cf365  /media/theremin/data  auto  defaults  0  2``` and update the UUID
1. Lastly, run ```sudo mkdir -p /media/theremin/data``` to make sure the directory is persistent
