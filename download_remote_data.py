'''
---
## References

OpenAI. (2025). ChatGPT (June 10th version) [Large language model]. https://chat.openai.com/chat

---

Running as a daemon

sudo nano /etc/systemd/system/csv_monitor.service

[Unit]
Description=Download Remote Data Daemon
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 /home/theremin/projects/instrument_data_acquisition/download_remote_data.py \
    --url https://coagmet.colostate.edu/data/latest/den01.csv?header=yes&dateFmt=iso&tz=utc&units=m&fields=t,rh,dewpt,vp,bp_avg,solarRad,rso,precip,wetb,dt,windSpeed,windDir,gustSpeed,gustDir \
    --folder /den01 \
    --prefix den01 \
    --interval  900
Restart=always
User=instrument
WorkingDirectory=/home/instrument/instrument_data_acquisition
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target

'''

'''
sudo systemctl daemon-reload
sudo systemctl enable download_remote_data.service
sudo systemctl start download_remote_data.service

# check status
systemctl status download_remote_data.service

'''


import requests
import csv
import time
import argparse
from datetime import datetime
from pathlib import Path

# Fetch CSV content from the provided URL and return the lines
def get_csv_lines(url):
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for HTTP errors
    return response.text.strip().splitlines()  # Return list of lines

# Save the header and a single line of data to the appropriate daily file
def save_to_daily_file(header, data_line, date_str, folder, prefix):
    filename = Path(folder) / f"{prefix}_{date_str}.csv"  # e.g., ./folder/prefix_2025-06-10.csv
    file_exists = filename.exists()  # Check if file already exists

    # Open the file in append mode, creating it if necessary
    with filename.open('a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(header)  # Write header only once per file/day
        writer.writerow(data_line)   # Append the data row

def main():
    # Define and parse command-line arguments
    parser = argparse.ArgumentParser(description="Monitor a CSV URL and save data daily.")
    parser.add_argument("--url", required=True, help="URL of the CSV file to monitor")
    parser.add_argument("--folder", required=True, help="Folder to save the CSV data files")
    parser.add_argument("--prefix", default="data", help="Prefix for saved CSV files")
    parser.add_argument("--interval", type=int, default=300, help="Interval in seconds between checks (default 300s)")

    args = parser.parse_args()  # Parse arguments from the command line

    # Ensure the target folder exists
    Path(args.folder).mkdir(parents=True, exist_ok=True)

    # Start the infinite loop to check every interval
    while True:
        try:
            current_date = datetime.now().strftime("%Y-%m-%d")  # Format today's date
            csv_lines = get_csv_lines(args.url)  # Fetch and read CSV
            reader = csv.reader(csv_lines)
            lines = list(reader)

            # Ensure there is at least a header and one data line
            if len(lines) < 2:
                print(f"[{datetime.now()}] CSV has fewer than 2 lines, skipping...")
            else:
                header = lines[0]         # First line is header
                second_line = lines[1]    # Second line is the desired data row
                save_to_daily_file(header, second_line, current_date, args.folder, args.prefix)
                print(f"[{datetime.now()}] Appended data to {args.prefix}_{current_date}.csv")

        except Exception as e:
            # Handle and log any error without crashing the script
            print(f"[{datetime.now()}] Error: {e}")

        time.sleep(args.interval)  # Wait for the specified interval before repeating

if __name__ == "__main__":
    main()  # Run the main function
