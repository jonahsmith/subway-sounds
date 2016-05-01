# trains.py
# Subway Sounds, written for Storytelling with Streaming Data, Columbia University
# May 2016
#
# This script contains a function, get_schedule(), that returns a dictionary of
# the next arrival and next departure times, in UTC, for the 1-2-3 platform and
# the S platform at the Times Square station in New York City. It uses the MTA's
# live GTFS feed.
#
# This script is not intended to be run on its own, but rather to be imported.
# It is currently imported by viewserver.py.

import requests
from google.transit import gtfs_realtime_pb2 as gtfs

# Grab the latest feed from the MTA
r = requests.get('http://datamine.mta.info/mta_esi.php?key=244af9c1c430895a314bcd995a0ba11c&feed_id=1')
# Initialize a feed object
feed = gtfs.FeedMessage()
# And load the feed object from the binary response
feed.ParseFromString(r.content)


# These are all of the code names for Times Square station, identified using the
# GTFS schedule data from the MTA (http://web.mta.info/developers/developer-data-terms.html)
times_square = ['127','127N', '127S', '725','725N','725S','902','902N','902S','R16','R16N','R16S']
# These are the train identifiers we are interested in. GS is the shuttle.
trains = ['1', '2', '3', 'GS']

# Initialize dictionaries to contain all of the arrival/departure times as an
# array for each route.
departures = {train: [] for train in trains}
arrivals = {train: [] for train in trains}

def get_schedule():
    """Return next arrival and departure time at 1-2-3 and S platforms, Times Square"""
    # Loop through the updates...
    for entity in feed.entity:
        # Make sure the update has actual update objects in it
        if entity.HasField('trip_update'):
            # For each update...
            for update in entity.trip_update.stop_time_update:
                route = entity.trip_update.trip.route_id
                # Check that: 1) the referenced stop is at Times Square, and 2)
                # the reference route is one of the ones we are interested in.
                if update.stop_id in times_square and route in trains:
                    # Some have arrival times, some have departure times; if it
                    # has one or both, add it to that route's entry in the
                    # arrival or departure dictionaries.
                    if update.HasField('arrival'):
                        arrivals[route].append(update.arrival.time)
                    if update.HasField('departure'):
                        departures[route].append(update.departure.time)

    # All of the following are in try blocks because min() returns a ValueError
    # when it receives an empty array. We'll catch that and just set the value
    # to None.
    #
    # They all work the same way. The timestamps are Unix epoch, so we can just
    # take the minimum to get the next scheduled one.
    try:
        soonest_departure_123 = min(departures['1'] + departures['2'] + departures['3'])
    except ValueError:
        soonest_departure_123 = None

    try:
        soonest_arrival_123 = min(arrivals['1'] + arrivals['2'] + arrivals['3'])
    except ValueError:
        soonest_arrival_123 = None

    try:
        soonest_departure_s = min(departures['GS'])
    except ValueError:
        soonest_departure_s = None

    try:
        soonest_arrival_s = min(arrivals['GS'])
    except ValueError:
        soonest_arrival_s = None

    # Generate the final data to return. A simple dictionary structure, with top
    # level keys corresponding to platform, and the next level of keys
    # corresponding to the next_arrival and next_departure.
    data = { '1-2-3': {
                        'next_arrival': soonest_arrival_123,
                        'next_departure': soonest_departure_123
                      },
             'S':     {
                        'next_arrival': soonest_arrival_s,
                        'next_departure': soonest_departure_s
                      }
    }

    return data
