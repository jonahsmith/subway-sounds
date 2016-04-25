import requests
import json

# The URL for the long-lived HTTP stream of sound intensity readings
URL = 'http://developer.usa.gov/1usagov'

# Establish redis connections, one for each level.


# Establish a connection to the long-lived HTTP stream
r = requests.get(URL, stream=True)

# Iterate through the messages in the stream indefinitely
for line in r.iter_lines():
    if line:
        print(json.loads(line))
