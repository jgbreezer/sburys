from __future__ import print_function
import argparse
import pprint

import dayinfo

def main():
    parser = argparse.ArgumentParser(description="Process day-value CSV file(s) and output weeks for each")
    parser.add_argument(action='store', dest='files', type=str, nargs="+")
    args = parser.parse_args()
    day_values = dayinfo.DayValue()
    for csv_filename in args.files:
        # Filename included in expected output from task description, assuming this is part of output.
        print(csv_filename)
        day_values.open_csv(open(csv_filename, "r"))
        for week_value in day_values.week_values():
            pprint.pprint(week_value)
        print()

if __name__ == "__main__":
    main()