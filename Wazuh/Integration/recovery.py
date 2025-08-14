#!/usr/bin/env python

import gzip
import time
import json
import argparse
import re
import os
from datetime import datetime
from datetime import timedelta

def log(msg):
    now_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    final_msg = "{0} wazuh-reinjection: {1}".format(now_date, msg)
    print(final_msg)
    if log_file:
        f_log.write(final_msg + "\n")

EPS_MAX = 400
wazuh_path = '/var/ossec/'
max_size=1
log_file = None

parser = argparse.ArgumentParser(description='Reinjection script')
parser.add_argument('-eps','--eps', metavar='eps', type=int, required = False, help='Events per second.')
parser.add_argument('-min', '--min_timestamp', metavar='min_timestamp', type=str, required = True, help='Min timestamp. Example: 2017-12-13T23:59:06')
parser.add_argument('-max', '--max_timestamp', metavar='max_timestamp', type=str, required = True, help='Max timestamp. Example: 2017-12-13T23:59:06')
parser.add_argument('-o', '--output_file', metavar='output_file', type=str, required = True, help='Output filename.')
parser.add_argument('-log', '--log_file', metavar='log_file', type=str, required = False, help='Logs output')
parser.add_argument('-w', '--wazuh_path', metavar='wazuh_path', type=str, required = False, help='Path to Wazuh. By default:/var/ossec/')
parser.add_argument('-sz', '--max_size', metavar='max_size', type=float, required = False, help='Max output file size in Gb. Default: 1Gb. Example: 2.5')

args = parser.parse_args()

if args.log_file:
    log_file = args.log_file
    f_log = open(log_file, 'a+')


if args.max_size:
    max_size = args.max_size

if args.wazuh_path:
    wazuh_path = args.wazuh_path

output_file = args.output_file

#Gb to bytes
max_bytes = int(max_size * 1024 * 1024 * 1024)

if (max_bytes <= 0):
    log("Error: Incorrect max_size")
    exit(1)

month_dict = ['Null','Jan','Feb','Mar','Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov','Dec']

if args.eps:
    EPS_MAX = args.eps

if EPS_MAX < 0:
    log("Error: incorrect EPS")
    exit(1)

min_date = re.search('(\\d\\d\\d\\d)-(\\d\\d)-(\\d\\d)T\\d\\d:\\d\\d:\\d\\d', args.min_timestamp)
if min_date:
    min_year = int(min_date.group(1))
    min_month = int(min_date.group(2))
    min_day = int(min_date.group(3))
else:
    log("Error: Incorrect min timestamp")
    exit(1)

max_date = re.search('(\\d\\d\\d\\d)-(\\d\\d)-(\\d\\d)T\\d\\d:\\d\\d:\\d\\d', args.max_timestamp)
if max_date:
    max_year = int(max_date.group(1))
    max_month = int(max_date.group(2))
    max_day = int(max_date.group(3))
else:
    log("Error: Incorrect max timestamp")
    exit(1)

# Converting timestamp args to datetime
min_timestamp = datetime.strptime(args.min_timestamp, '%Y-%m-%dT%H:%M:%S')
max_timestamp = datetime.strptime(args.max_timestamp, '%Y-%m-%dT%H:%M:%S')

chunk = 0
written_alerts = 0
trimmed_alerts = open(output_file, 'w')

max_time=datetime(max_year, max_month, max_day)
current_time=datetime(min_year, min_month, min_day)

while current_time <= max_time:
    alert_file = "{0}logs/alerts/{1}/{2}/ossec-alerts-{3:02}.json.gz".format(wazuh_path,current_time.year,month_dict[current_time.month],current_time.day)

    if os.path.exists(alert_file):
        daily_alerts = 0
        compressed_alerts = gzip.open(alert_file, 'r')
        log("Reading file: "+ alert_file)
        for line in compressed_alerts:
            # Transform line to json object
            try:
                line_json = json.loads(line.decode("utf-8", "replace"))

                # Remove unnecessary part of the timestamp
                string_timestamp = line_json['timestamp'][:19]

                # Ensure timestamp integrity
                while len(line_json['timestamp'].split("+")[0]) < 23:
                    line_json['timestamp'] = line_json['timestamp'][:20] + "0" + line_json['timestamp'][20:]

                # Get the timestamp readable
                event_date = datetime.strptime(string_timestamp, '%Y-%m-%dT%H:%M:%S')

                # Check the timestamp belongs to the selected range
                if (event_date <= max_timestamp and event_date >= min_timestamp):
                    chunk+=1
                    trimmed_alerts.write(json.dumps(line_json))
                    trimmed_alerts.write("\n")
                    trimmed_alerts.flush()
                    daily_alerts += 1
                    if chunk >= EPS_MAX:
                        chunk = 0
                        time.sleep(2)
                    if os.path.getsize(output_file) >= max_bytes:
                        trimmed_alerts.close()
                        log("Output file reached max size, setting it to zero and restarting")
                        time.sleep(EPS_MAX/100)
                        trimmed_alerts = open(output_file, 'w')

            except ValueError as e:
                print("Oops! Something went wrong reading: {}".format(line))
                print("This is the error: {}".format(str(e)))

        compressed_alerts.close()
        log("Extracted {0} alerts from day {1}-{2}-{3}".format(daily_alerts,current_time.day,month_dict[current_time.month],current_time.year))
    else:
        log("Couldn't find file {}".format(alert_file))

    #Move to next file
    current_time += timedelta(days=1)

trimmed_alerts.close()
