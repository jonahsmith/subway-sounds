import requests
import json
from sys import stdout
from datetime import datetime 

# The URL for the long-lived HTTP stream of sound intensity readings
URL = 'http://localhost:6998'

# Establish redis connections, one for each level.


# Establish a connection to the long-lived HTTP stream
r = requests.get(URL, stream=True)

# Iterate through the messages in the stream indefinitely
for line in r.iter_lines(chunk_size=10):
    if line:
        data = json.loads(line)
        print data, datetime.now()
        stdout.flush()
