import json
import os
from haralyzer import HarParser
import dateutil.parser
import matplotlib.pyplot as plt

data = []

for filename in os.listdir(os.getcwd()):
    if filename == "graph.py":
        continue
    with open(filename, 'r') as f:
        har_parser = HarParser(json.loads(f.read()))
	max = len(har_parser.pages[0].entries)
	start_time = har_parser.pages[0].entries[0]["startedDateTime"]
	end_time =  har_parser.pages[0].entries[max - 1]["startedDateTime"]
	end_load = float(har_parser.pages[0].entries[max - 1]["time"]) / 1000
	diff = dateutil.parser.parse(end_time) - dateutil.parser.parse(start_time)
	data.append((diff.total_seconds()) + end_load)

sorted_data = sorted(data, key=float, reverse=True)
num = list(range(1, len(data)+1))
print(num)
plt.scatter(num, sorted_data)
plt.xlabel('Number of experiments')
plt.ylabel('Page loading times')
plt.show()
