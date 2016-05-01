

import redis
import json
import time
from datetime import datetime, timedelta, date
from sys import stdout
import trains


PAUSE = 5

def create_history(date):
    history = {
                'max': {level: make_reading((None, 0)) for level in ['street', 's', 'red', 'purple']},
                'min': {level: make_reading((None, 999)) for level in ['street', 's', 'red', 'purple']},
                'date': date
              }
    return history


def make_reading(val):
    return {'time': val[0], 'value': val[1]}


def get_values(database):
    keys = database.keys()
    values = database.mget(keys)
    key_val = [(int(key), float(val)) for key, val in zip(keys, values) if val]
    return key_val


def get_stats(level_name, values):
    now_min = min(values, key=lambda kv: kv[1])
    now_max = max(values, key=lambda kv: kv[1])
    most_recent = max(values, key=lambda kv: kv[0])

    if today['max'][level_name]['value'] < now_max[1]:
        today['max'][level_name] = make_reading(now_max)

    if today['min'][level_name]['value'] > now_min[1]:
        today['min'][level_name] = make_reading(now_min)

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



def get_trains():
    return trains.get_schedule()


def global_setup():
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


def main():
    while 1:
        global today, yesterday

        if today['date'] != date.today():
            yesterday = today
            reset_history(today, date.today())

        street_stats = get_stats('street', get_values(street))
        s_stats = get_stats('s', get_values(s))
        red_stats = get_stats('red', get_values(red))
        purple_stats = get_stats('purple', get_values(purple))

        trains = get_trains()

        s_stats['trains'] = trains['S']
        red_stats['trains'] = trains['1-2-3']

        payload = {
                    'surface': street_stats,
                    'concourse': s_stats,
                    '1-2-3': red_stats,
                    '7': purple_stats
                  }
        print(json.dumps(payload))
        stdout.flush()
        time.sleep(PAUSE)


if __name__ == '__main__':
    global_setup()
    main()
