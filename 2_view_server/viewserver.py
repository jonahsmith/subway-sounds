# viewserver.py
# Subway Sounds, written for Storytelling with Streaming Data, Columbia University
# May 2016
#
# This script queries the Redis database to compute statistics on the most
# recent data, gets the train schedule from trains.py, and sends the data as a
# JSON string to stdout, where it is to be picked up by websocketd and broadcast
# over a websocket. This is done every PAUSE seconds.

import redis
import json
import time
from datetime import datetime, timedelta, date
from sys import stdout
# This is our module, also in this directory, that returns the next arrival and
# departure for a particular platform.
import trains


# This is a global configuration variable that specifies the number of seconds
# between updates. (In concrete terms, this will specify how often the data on
# the client's page updates.)
PAUSE = 5

def create_history(date):
    """A factory function for historical data containers"""
    history = {
                'max': {level: make_reading((None, 0)) for level in ['street', 's', 'red', 'purple']},
                'min': {level: make_reading((None, float('inf'))) for level in ['street', 's', 'red', 'purple']},
                'date': date
              }
    return history


def make_reading(val):
    """Given a tuple, return a dictionary in the format of 'measurement' nodes."""
    return {'time': val[0], 'value': val[1]}


def get_values(database):
    """Return (key, value) tuples for every entry in the given Redis database"""
    keys = database.keys()
    values = database.mget(keys)
    # This removes entries that expired between retrieving the keys and
    # retrieving the values. This is one option for dealing with the sequential
    # retrieval of keys and values. Given the rate of the stream, this should
    # not be more than one entry, if any, meaning it has minimal impact. It also
    # does not affect the story much, as it just means that an older reading has
    # expired.
    key_val = [(int(key), float(val)) for key, val in zip(keys, values) if val]
    return key_val


def get_stats(level_name, values):
    """Calculate the min/max over three time scales: Redis TTL, today, yesterday"""
    # Given all of the values from Redis, we find the min/max. In practical
    # terms, that means the minimum over the TTL for the database.
    now_min = min(values, key=lambda kv: kv[1])
    now_max = max(values, key=lambda kv: kv[1])
    # This is the most recent reading. We can do this because the timestamps are
    # epoch timestamps, e.g. we can just sort for the largest to get the most
    # recent.
    most_recent = max(values, key=lambda kv: kv[0])

    # Update today's max and min, if the current values are more extreme than
    # the previously most extreme.
    if today['max'][level_name]['value'] < now_max[1]:
        today['max'][level_name] = make_reading(now_max)

    if today['min'][level_name]['value'] > now_min[1]:
        today['min'][level_name] = make_reading(now_min)

    # Construct our data structure using the statistics we've just computed.
    # This is the schema used by the front end.
    data = {
            'current': make_reading(most_recent),
            'current_peak': make_reading(now_max),
            'current_trough': make_reading(now_min),
            'today_peak': today['max'][level_name],
            'today_trough': today['min'][level_name],
            'yest_peak': yesterday['max'][level_name],
            'yest_trough': yesterday['min'][level_name]
           }

    return data


def global_setup():
    """Initialize global data structures (Redis connections and history)"""
    # Establish the historical data dictionaries
    global today, yesterday
    today = create_history(date.today())
    yesterday = create_history(date.today() - timedelta(days=1))

    # Establish redis connections, one table for each level.
    global street, s, red, purple
    street = redis.Redis(db=0)
    s = redis.Redis(db=1)
    red = redis.Redis(db=2)
    purple = redis.Redis(db=3)


def send():
    """Send statistics via stdout every PAUSE seconds"""
    # Repeat indefinitely
    while 1:
        global today, yesterday

        # If the date in the 'today' history log is not actually today, that
        # means it's just past midnight. As such, we need to move today's into
        # yesterday, and reset today's.
        if today['date'] != date.today():
            yesterday = today
            today = reset_history(date.today())

        # Calculate the statistics for each level
        street_stats = get_stats('street', get_values(street))
        s_stats = get_stats('s', get_values(s))
        red_stats = get_stats('red', get_values(red))
        purple_stats = get_stats('purple', get_values(purple))

        # Get the next arriving and departing trains using our library
        train_times = trains.get_schedule()
        # and add them to the data for those platforms
        s_stats['trains'] = train_times['S']
        red_stats['trains'] = train_times['1-2-3']

        # Construct the data structure for the JSON string.
        payload = {
                    'surface': street_stats,
                    'concourse': s_stats,
                    '1-2-3': red_stats,
                    '7': purple_stats
                  }
        # Print it to stdout
        print(json.dumps(payload))
        # Flush to prevent buffering
        stdout.flush()
        # Pause for PAUSE time before repeating.
        time.sleep(PAUSE)


if __name__ == '__main__':
    # When we start up this file, initialize the global files...
    global_setup()
    # Then start the indefinite loop sending data to stdout
    send()
