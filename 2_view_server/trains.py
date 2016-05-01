import requests
from google.transit import gtfs_realtime_pb2 as gtfs

r = requests.get('http://datamine.mta.info/mta_esi.php?key=244af9c1c430895a314bcd995a0ba11c&feed_id=1')
feed = gtfs.FeedMessage()
feed.ParseFromString(r.content)


times_square = ['127','127N', '127S', '725','725N','725S','902','902N','902S','R16','R16N','R16S']
trains = ['1', '2', '3', 'GS']

departures = {train: [] for train in trains}
arrivals = {train: [] for train in trains}

def get_schedule():
    for entity in feed.entity:
        if entity.HasField('trip_update'):
            for update in entity.trip_update.stop_time_update:
                route = entity.trip_update.trip.route_id
                if update.stop_id in times_square and route in trains:
                    if update.HasField('arrival'):
                        arrivals[route].append(update.arrival.time)
                    if update.HasField('departure'):
                        departures[route].append(update.departure.time)

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
