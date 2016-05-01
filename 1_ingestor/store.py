# store.py
# Subway Sounds, written for Storytelling with Streaming Data, Columbia University
# May 2016
#
# This script receives the data stream from stdin and stores it in a Redis
# database serving over the default port (6379). For easy querying, timestamps
# are used as the keys.
#
# The TTL is currently set to 5 minutes. This decision is discussed at length in
# our methodology; for here, suffice it to say that, among other reasons, it was
# selected because it would be a reasonable amount of time for someone to spend
# on a particular platform.

import json
import redis
from sys import stdin

# The amount of time for which values should persist, in seconds
TTL = 5*60

# Establish redis connections, one table for each level
street = redis.Redis(db=0)
s = redis.Redis(db=1)
red = redis.Redis(db=2)
purple = redis.Redis(db=3)

# Iterate through the messages in the stream indefinitely
while 1:
    # Read the line
    line = stdin.readline()
    # Parse the string as JSON
    data = json.loads(line)

    # Pull out the timestamp, to be used as keys in all of the tables
    timestamp = data['time']

    # Add the new readings to the Redis database with TTL defined above
    street.setex(timestamp, data['readings']['street'], TTL)
    s.setex(timestamp, data['readings']['s'], TTL)
    red.setex(timestamp, data['readings']['1-2-3'], TTL)
    purple.setex(timestamp, data['readings']['7'], TTL)
