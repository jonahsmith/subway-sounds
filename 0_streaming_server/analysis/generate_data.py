from spl import getdecibels
from sys import argv, exit
import os
import json

try:
    directory = argv[1]
except IndexError:
    print('No data directory given.')
    exit(1)

files = os.listdir(directory)

if not os.path.exists(os.path.join(directory, 'processed-data/')):
    os.mkdir(os.path.join(directory, 'processed-data/'))


for f in files:
    path = os.path.join(directory, f)
    print('Processing: {}'.format(path))
    try:
        dbs, dbs_a = getdecibels(path, chunk_factor=60)
        data = {'path': path, "Original": dbs, "A-weighted": dbs_a}
        with open(os.path.join(directory, 'processed-data/', f + '.json'),'w') as outfile:
        	json.dump(data, outfile)
    except:
        print('Something went wrong processing {}'.format(path))
