import requests
import json
from sys import stdout
from datetime import datetime
import redis

# The URL for the long-lived HTTP stream of sound intensity readings
URL = 'http://localhost:6998'

# The amount of time for which values should persist, in seconds
TTL = 15*60

# Establish redis connections, one table for each level.
street = redis.Redis(db=0)
s = redis.Redis(db=1)
red = redis.Redis(db=2)
purple = redis.Redis(db=3)

# Establish a connection to the long-lived HTTP stream
r = requests.get(URL, stream=True)

# Iterate through the messages in the stream indefinitely
for line in r.iter_lines():
    if line:
        data = json.loads(line)
        timestamp = data['time']

        # Add the new readings to the Redis database
        street.setex(timestamp, data['readings']['street'], TTL)
        s.setex(timestamp, data['readings']['s'], TTL)
        red.setex(timestamp, data['readings']['1-2-3'], TTL)
        purple.setex(timestamp, data['readings']['7'], TTL)
