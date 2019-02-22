import datetime
import json
import time

import math

b = "21/03/2018"
e = "22/03/2018"

begin = time.mktime(datetime.datetime.strptime(b, "%d/%m/%Y").timetuple())
end = time.mktime(datetime.datetime.strptime(e, "%d/%m/%Y").timetuple())

# print((end-begin)/24/12)
#
# for i in range(start=begin, stop=end, step=300):
#

print(begin)
print(end)


data = [
    {
        'time': begin,
        'datapoints': [
            {'name': 'John Bolton', 'value': 0.542},
            {'name': 'trend1', 'value': 0.421},
            {'name': 'trend two', 'value': 0.222123}
        ]
    },
    {
        'time': begin + 300,
        'datapoints': [
            {'name': 'John Bolton', 'value': 0.33},
            {'name': 'trend1', 'value': 0.543},
            {'name': 'trend two', 'value': 0.2}
        ]
    },
    {
        'time': begin + 600,
        'datapoints': [
            {'name': 'John Bolton', 'value': 0.23},
            {'name': 'trend1', 'value': 0.654},
            {'name': 'trend two', 'value': 0.222123}
        ]
    },
    {
        'time': begin + 900,
        'datapoints': [
            {'name': 'John Bolton', 'value': 0.20001},
            {'name': 'trend1', 'value': 0.654},
            {'name': 'trend two', 'value': 0.199}
        ]
    },
    {
        'time': begin + 900,
        'datapoints': [
            {'name': 'John Bolton', 'value': 0.20001},
            {'name': 'trend1', 'value': 0.654},
            {'name': 'trend two', 'value': 0.1}
        ]
    },
    {
        'time': begin + 1200,
        'datapoints': [
            {'name': 'Madonna', 'value': 0.11},
            {'name': 'John Bolton', 'value': 0.19},
            {'name': 'trend1', 'value': 0.7},
        ]
    },
    {
        'time': begin + 1500,
        'datapoints': [
            {'name': 'Madonna', 'value': 0.24},
            {'name': 'John Bolton', 'value': 0.17},
            {'name': 'trend1', 'value': 0.71},
        ]
    },
    {
        'time': begin + 1800,
        'datapoints': [
            {'name': 'Madonna', 'value': 0.29},
            {'name': 'John Bolton', 'value': 0.1},
            {'name': 'trend1', 'value': 0.77},
        ]
    },
    {
        'time': begin + 2100,
        'datapoints': [
            {'name': 'Madonna', 'value': 0.2},
            {'name': 'trend1', 'value': 0.4},
        ]
    },
    {
        'time': begin + 2400,
        'datapoints': [
            {'name': 'Madonna', 'value': 0.12},
            {'name': 'Trump', 'value': 0.13},
            {'name': 'trend1', 'value': 0.15},
        ]
    },
    {
        'time': begin + 2700,
        'datapoints': [
            {'name': 'Trump', 'value': 0.22},
        ]
    },
    {
        'time': begin + 3000,
        'datapoints': [
            {'name': 'Trump', 'value': 0.3},
            {'name': 'Lucas Film', 'value': 0.13},
            {'name': 'Tango in Harlem', 'value': 0.15},
        ]
    }

]

with open('example_alltogether.json', 'w+') as f:
    f.write(json.dumps(data))
