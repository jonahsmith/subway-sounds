import time
from sys import stdout
import json
from random import random

while 1:
    print(json.dumps( {
                        'street': int(random()*100),
                        's': int(random()*1000),
                        '1-2-3': int(random()*1000),
                        '7': int(random()*1000)
                      }
                    )
          )
    stdout.flush()
    time.sleep(2)
