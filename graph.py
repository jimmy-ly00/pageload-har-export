import json
import os
from haralyzer import HarParser
import dateutil.parser
import datetime
import numpy as np
import matplotlib.pyplot as plt

def scan_files(path):
    data = []
    # Parse all files in directory
    for filename in os.listdir(path):
        with open(os.path.join(path, filename), 'r') as f:
            har_parser = HarParser(json.loads(f.read()))

        start_time = dateutil.parser.parse(har_parser.pages[0].entries[0]["startedDateTime"]) 
        latest_time = start_time
        
        # Parse all resources HTML, CSS, JS...
        for entry in (har_parser.pages[0].entries):
            if entry["time"] == None:
                s = 0
            else:
                s = float(entry["time"])/1000

            current_time = dateutil.parser.parse(entry["startedDateTime"]) + datetime.timedelta(seconds = s)
            if (current_time > latest_time):
                latest_time = current_time
      
        total = latest_time - start_time
        #if total > datetime.timedelta(seconds = 100):
        #    os.remove(os.path.join(path, filename))

        data.append(total.total_seconds())
    return data

def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)

def main():
    a = scan_files(os.getcwd() + '/traditionalnodelay1')
    b = scan_files(os.getcwd() + '/angularnodelay1')
#    c = scan_files(os.getcwd() + '/inline')
    
    sorted_a = sorted(a, key=float, reverse=True)
    sorted_b = sorted(b, key=float, reverse=True)
#    sorted_c = sorted(c, key=float, reverse=True)
    #print(sorted_data)
    
    num_a = list(range(1, len(a)+1))
    num_b = list(range(1, len(b)+1))
#    num_c = list(range(1, len(b)+1))

    # Plot scatter
    plt.scatter(num_a, sorted_a, label="Traditional", marker="o", s=12)
    plt.scatter(num_b, sorted_b, label="Angular", marker="^", s=12)
#    plt.scatter(num_b, sorted_c, label="Inline", marker="s", s=12)
    plt.legend(loc='upper right')
    plt.xlabel('Number of experiments')
    plt.ylabel('Page loading times (seconds)')

    # Plot histogram
#    plt.hist(sorted_c, normed=True, facecolor='green', bins=15)
#    plt.xlabel('Page loding times (seconds)')
#    plt.ylabel('Frequency')
    
    # Plot bar chart
#    a = scan_files(os.getcwd() + '/traditionalnodelay1')
#    b = scan_files(os.getcwd() + '/angularnodelay1')

#    objects = ('Traditional', 'AngularJS')
#    y_pos = np.arange(len(objects))
#    performance = [mean(a), mean(b)]
#    plt.bar(y_pos, performance,0.5, align='center', alpha=0.5)
#    plt.xticks(y_pos, objects)
#    plt.ylabel('Mean loading times (seconds)')

    plt.show()

if __name__ == "__main__":
    main()


