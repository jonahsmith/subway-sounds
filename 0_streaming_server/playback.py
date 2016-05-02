"""
playback.py

Take data from the pre-made JSON files and serve it as a real time data.

We do this by iterating through the data in an infinite loop, and printing out
a JSON dump onto the stdout for some other process to consume. If we reach the
end of the list, we just start from the beginning.
"""

import time
from sys import stdout, exit, argv
import json
import time
import os

time_per_chunk = 1


def calibrate(value, calibration_constant = -6, round_off=2):
    """
    Calibration function.

    Takes in a single value and return a calibrated value.

    In our case, we subtract 6 from the reading and round off to the neareset 2nd digit
    """
    return round(float(value) - calibration_constant,round_off)

# The argument to the python file is the day for which we wish to render out the redings
try:
    if argv[1] not in ('day1', 'day2'):
        print('Specify either "day1" or "day2"')
        exit(1)
    else:
        day = argv[1]
except IndexError:
    day = 'day1'

basepath = os.path.join('analysis', day, 'processed-data/')



# Open the files and store the JSON data in a variable called static_data
static_data = {}
for f in ['1_street.WAV.json', '2_concourse.WAV.json', '3_1-2-3.WAV.json', '4_7.WAV.json']:
    with open(os.path.join(basepath, f)) as datafile:
        static_data[f] = json.load(datafile)

#find the smallest run length we have
total = len(static_data[min(static_data, key=lambda k: len(static_data[k]))]['A-weighted'])



# start with the first reading
index = 0

while 1:
    if index >= total:
        index = 0
    data = {}
    data['time'] = int(time.time()) # We use UNIX epoch time. Since the standard datetime has issues with JSON
    data['readings'] = {}
    data['readings']['street'] = static_data['1_street.WAV.json']['A-weighted'][index]
    data['readings']['s'] = static_data['2_concourse.WAV.json']['A-weighted'][index]
    data['readings']['1-2-3'] = static_data['3_1-2-3.WAV.json']['A-weighted'][index]
    data['readings']['7'] = static_data['4_7.WAV.json']['A-weighted'][index]


    #Apply calibration to the reading

    for level in data['readings']:
        data['readings'][level] = calibrate(data['readings'][level])
    print(json.dumps(data))

    index +=1
    time.sleep(time_per_chunk)
    stdout.flush()
