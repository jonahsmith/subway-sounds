# ingest.py
# Subway Sounds, written for Storytelling with Streaming Data, Columbia University
# May 2016
#
# This file connects to a long-lived HTTP stream of sound intensity readings and
# outputs each message to stdout. This file is separate under the idea that, if
# the MTA were to open a data stream of sound intensity, this could be swapped
# with a script to ingest that stream, and the rest of the scripts could remain
# the same (e.g. this is the only file that would need to change.)
#
# This file is intended to be piped into store.py.

import requests
from sys import stdout

# The URL for the long-lived HTTP stream of sound intensity readings
URL = 'http://localhost:6998'

# Make the get request to the long-lived HTTP stream
r = requests.get(URL, stream=True)

# Iterate through the messages in the stream indefinitely
for line in r.iter_lines():
    # Filter out empty lines, in case a blank message is sent through.
    if line:
        print(line)
        stdout.flush()
