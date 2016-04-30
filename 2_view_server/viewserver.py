

import redis
import json
import time
from datetime import datetime, timedelta, date
from sys import stdout


PAUSE = 5

# Establish redis connections, one table for each level.
street = redis.Redis(db=0)
s = redis.Redis(db=1)
red = redis.Redis(db=2)
purple = redis.Redis(db=3)


today = {}
yesterday = {}

reset_history(today, date.now())
reset_history(yesterday, date.now() - timedelta(days=1))

def reset_history(day, date):
    days = {
            'max': {level: make_reading((None, 0)) for level in ['street', 's', 'red', 'purple']},
            'min': {level: make_reading((None, 0)) for level in ['street', 's', 'red', 'purple']}
            }
    day['date'] = date


def make_reading(val):
    return {'time': val[0], 'value': val[1]}


def get_values(database):
    keys = database.keys()
    values = database.mget(keys)
    key_val = [(int(key), float(val)) for key, val in zip(keys, values) if val)]
    return key_val


def get_stats(level_name, values):
    now_min = min(values, key=lambda kv: return kv[1])
    now_max = max(values, key=lambda kv: return kv[1])
    most_recent = max(values, key=lambda kv: return kv[0])

    if today[level_name]['max']['value'] < now_max[1]:
        today[level_name]['max'] = make_reading(now_max)

    if today[level_name]['min']['value'] > now_min[1]:
        today[level_name]['min'] = make_reading(now_min)

    data = {
            'current': make_reading(most_recent),
            'current_peak': make_reading(now_max),
            'current_trough': make_reading(now_min),
            'today_peak': today[level_name]['max'],
            'today_trough': today[level_name]['min'],
            'yest_peak': yesterday[level_name]['max'],
            'yest_trough': yesterday[level_name]['min']
           }

    return data


while 1:
    global today
    global yesterday

    if today['date'] != date.today():
        yesterday = today
        reset_history(today, date.today())

    street_stats = get_stats('street', get_values(street))
    s_stats = get_stats('s', get_values(s))
    red_stats = get_stats('red', get_values(red))
    purple_stats = get_stats('purple', get_values(purple))

    payload = {
                'surface': street_stats,
                'concourse': s_stats,
                '1-2-3': red_stats,
                '7': purple_stats
              }
    print(json.dumps(payload))
    stdout.flush()
    time.sleep(PAUSE)
