#!/usr/bin/env python3

"""
## References

OpenAI. (2026). ChatGPT (June 10th version) [Large language model]. https://chat.openai.com/chat

---

Download daily 5-minute CoAgMet data as individual CSV files.

Example:
    python download_coagmet_daily_data.py \
        --start 2026-03-01 \
        --end 2026-03-05 \
        --folder /home/theremin/projects/den01 \
        --prefix den01

"""

import argparse
from datetime import datetime, timedelta
from pathlib import Path
import requests
import sys


BASE_URL = "https://coagmet.colostate.edu/data/5min/den01.csv"

FIELDS = "t,rh,dewpt,vp,bp_avg,solarRad,rso,precip,wetb,dt,windSpeed,windDir,gustSpeed,gustDir"


def fetch_day(date, folder, prefix):
    """
    Fetch data for a single day and save to CSV.
    Removes second header row (units) if present.
    """
    next_day = date + timedelta(days=1)

    from_str = date.strftime("%Y-%m-%d")
    to_str = next_day.strftime("%Y-%m-%d")

    params = {
        "header": "yes",
        "from": from_str,
        "to": to_str,
        "dateFmt": "iso",
        "tz": "utc",
        "units": "m",
        "fields": FIELDS,
    }

    filename = Path(folder) / f"{prefix}_{from_str}.csv"

    try:
        response = requests.get(BASE_URL, params=params, timeout=30)
        response.raise_for_status()

        lines = response.text.splitlines()

        # 🔍 Detect and remove second header row (units row)
        if len(lines) > 1:
            second_line = lines[1].lower()

            # Heuristic: units row contains measurement units
            unit_indicators = ["deg", "%", "kpa", "m/s", "w m-2", "mm", "hpa"]

            if any(unit in second_line for unit in unit_indicators):
                print(f"Removing units row for {from_str}")
                lines.pop(1)

        # Write cleaned file
        with open(filename, "w") as f:
            f.write("\n".join(lines) + "\n")

        print(f"Saved: {filename}")

    except requests.exceptions.RequestException as e:
        print(f"Failed for {from_str}: {e}", file=sys.stderr)


def daterange(start_date, end_date):
    """
    Generator for iterating over dates.
    """
    current = start_date
    while current < end_date:
        yield current
        current += timedelta(days=1)


def main():
    parser = argparse.ArgumentParser(description="Download CoAgMet daily CSV data.")

    parser.add_argument("--start", required=True, help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", required=True, help="End date (YYYY-MM-DD)")
    parser.add_argument("--folder", required=True, help="Output folder")
    parser.add_argument("--prefix", required=True, help="Filename prefix")

    args = parser.parse_args()

    # Convert dates
    start_date = datetime.strptime(args.start, "%Y-%m-%d")
    end_date = datetime.strptime(args.end, "%Y-%m-%d")

    # Create folder if it doesn't exist
    output_dir = Path(args.folder)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"Downloading data from {args.start} to {args.end}...")

    for date in daterange(start_date, end_date):
        fetch_day(date, output_dir, args.prefix)

    print("Done.")


if __name__ == "__main__":
    main()