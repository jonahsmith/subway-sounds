import time
from sys import stdout
import json
# from random import random
import time
from data import concourse_2_60, train_1_2_3_day_1_60, train_1_2_3_day_2_60, weekday_day1

chunks_per_minute = 60




time_per_chunk = 60/chunks_per_minute



total = min(len(concourse_2_60),len(train_1_2_3_day_1_60),len(train_1_2_3_day_2_60),len(weekday_day1))


print total

index = 0
while 1:
    if index >= total:
        index = 0
    data = {}
    data['time'] = index*time_per_chunk
    data['readings'] = {}
    data['readings']['street'] = weekday_day1[index]
    data['readings']['s'] = concourse_2_60[index]
    print(json.dumps(data))

    index +=1
    time.sleep(time_per_chunk)
    stdout.flush()
    # time.sleep(2)
