#!/bin/env python
"""
Generate a report making it easy to transfer :spend lines to the tracker.

Outputs to stdout the categories and the spend times for them,
suitable for cut/pasting into a tracker issue.
"""


import argparse
from datetime import datetime
from datetime import timedelta
from collections import defaultdict
import json
import os
import os.path
import sys


def build_parser():
    """
    Collect command line arguments.
    """
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('-m', '--months_ago', type=int,
                        default=1,
                        help='Number of months ago to report on. Default: %(default)s')
    return parser


def compute_initial_date(months_ago):
    now = datetime.now()
    month = now.month - months_ago
    year = now.year
    while month < 1:
        month = month + 12
        year = year - 1
    return now.replace(year=year, month=month, day=1, hour=0, minute=0, second=0, microsecond=0)


def get_day_data_path(date):
    """
    Get the data path for a specific date.
    """
    home = os.environ.get('USERPROFILE').replace('\\', '/')
    data_dir= os.path.join(home, 'TimeData')
    if not os.path.isdir(data_dir):
        mkdir(data_dir)
    filename_date = date.strftime('%Y-%m-%d')
    then_filename = os.path.join(data_dir, filename_date + '.json')
    return then_filename, filename_date


def main(args):
    initial_date = compute_initial_date(args.months_ago)
    month = initial_date.month
    this_date = initial_date
    month_data = defaultdict(list)
    while this_date.month == month:
        try:
            (filename, spend_date) = get_day_data_path(this_date)
            with open(filename) as file:
                data = json.load(file)
                for d in data:
                    if d['time'] == '0:00:00':
                        # No time spent - ignore.
                        continue
                    t = datetime.strptime(d['time'], '%H:%M:%S')
                    m = t.hour * 60 + t.minute + t.second / 60
                    month_data[d['category']].append(':spend %2.2fm %s' % (m, spend_date))
        except FileNotFoundError:
            # Ignore missing files. Probably weekends.
            pass
        this_date += timedelta(1)
    for k in sorted(month_data.keys()):
        print(k)
        print('\n'.join( month_data[k]))


if __name__ == '__main__':
    sys.exit(main(build_parser().parse_args()))
