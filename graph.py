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
        # if total < datetime.timedelta(seconds = 1000):
			# os.remove(os.path.join(path, filename))
			# print(filename)
			
        data.append(total.total_seconds()*1000)
    return data

############ Bar chart alternate with error bars#############
def bar():
	a = scan_files(os.getcwd() + '/traditional_nodelay')
	b = scan_files(os.getcwd() + '/traditional_delay')
	c = scan_files(os.getcwd() + '/angular_nodelay')
	d = scan_files(os.getcwd() + '/angular_delay')

	bar_width = 0.3
	objects = ('Without delay', 'With delay')
	index = np.arange(len(objects))

	traditional_mean = [np.mean(a), np.mean(b)] 
	traditional_std = [np.std(a), np.std(b)]
	angular_mean = [np.mean(c), np.mean(d)]
	angular_std = [np.std(c), np.std(d)]

	plt.bar(index, traditional_mean, bar_width, align='center', yerr=traditional_std, capsize=5, alpha=0.5, label="Multi-page Application")
	plt.bar(index + bar_width, angular_mean, bar_width, align='center', yerr=angular_std, capsize=5, alpha=0.5, label="Single-page Application")
	ax = plt.axes() 
	ax.yaxis.grid(alpha=0.2)
	plt.legend(loc='upper left')
	plt.xticks(index + bar_width / 2, objects)
	plt.ylabel('Mean page loading times (ms)')
	plt.show()
	
	
############ Bar chart separate with error bars#############
# def bar():
	# # a = scan_files(os.getcwd() + '/traditional_nodelay')
	# # b = scan_files(os.getcwd() + '/angular_nodelay')
	# a = scan_files(os.getcwd() + '/traditional_delay')
	# b = scan_files(os.getcwd() + '/angular_delay')
	
	# bar_width = 0.3
	# objects = ('Multi-page Application', 'Single-page Application')
	# index = np.arange(len(objects))
	
	# # performance = [np.mean(a), np.mean(b)]
	# # std = [np.std(a), np.std(b)]

	# plt.bar(index, performance, bar_width, align='center', yerr=std, capsize=5, alpha=0.5)
	# ax = plt.axes() 
	# ax.yaxis.grid(alpha=0.2)
	# plt.xticks(index, objects)
	# plt.ylabel('Mean page loading times (ms)')
	# plt.show()

##################### CDF ##########################
def cdf():
	# # Emperical
	# bins = 500
	# plt.hist(a, bins, normed=True, cumulative=True, label='Multi-page Application', histtype='step', alpha=0.55, color='purple')
	# plt.hist(b, bins, normed=True, cumulative=True, label='Single-page Application', histtype='step', alpha=0.55, color='purple') 

	## MPA vs SPA
	# a = scan_files(os.getcwd() + '/traditional_delay')
	# b = scan_files(os.getcwd() + '/angular_delay')
	
	## MPA + About vs SPA
	# temp_0 = scan_files(os.getcwd() + '/traditional_delay')
	# temp_1 = scan_files(os.getcwd() + '/traditional_about_delay')
	# a = [(x + y) for x, y in zip(temp_0, temp_1)]
	# b = scan_files(os.getcwd() + '/angular_delay')
	
	# Normal vs Webpack vs Silo
	a = scan_files(os.getcwd() + '/angular_delay')
	b = scan_files(os.getcwd() + '/angular_webpack_delay_1')
	c = scan_files(os.getcwd() + '/angular_inline_delay')
	
	n = 100
	sorted_a = np.sort(a)
	sorted_b = np.sort(b)
	sorted_c = np.sort(c)
	h, x1 = np.histogram(sorted_a, bins = 100, normed = True)
	h, x2 = np.histogram(sorted_b, bins = 100, normed = True)
	h, x3 = np.histogram(sorted_c, bins = 100, normed = True)
	dx = x1[1] - x1[0]
	dx = x2[1] - x2[0]
	dx = x3[1] - x3[0]
	cdf_a = np.cumsum(h)*dx
	cdf_b = np.cumsum(h)*dx
	cdf_c = np.cumsum(h)*dx
	
	plt.figure(1, figsize=(8,4))
	#plt.plot(x1[1:], cdf_a, label="Multi-page Application")
	#plt.plot(x2[1:], cdf_b, label="Single-page Application", linestyle='--')
	plt.plot(x1[1:], cdf_a, label="Normal",)
	plt.plot(x2[1:], cdf_b, label="Webpack", linestyle='--')
	plt.plot(x3[1:], cdf_c, label="Silo", linestyle=':')
	
	plt.grid(alpha=0.2)
	plt.legend(loc='upper left', prop={'size': 9})
	plt.ylabel('CDF')
	plt.xlabel('Page loading times (ms)')
	
	plt.show()
	
def scatter():
	a = scan_files(os.getcwd() + '/angular_webpack_delay_1')
	sorted_a = np.sort(a)
	num_a = list(range(1, len(a)+1))
    
	plt.scatter(num_a, sorted_a, label="angular_silo_delay", marker="o", s=12)
	plt.legend(loc='upper right')
	plt.xlabel('Number of experiments')
	plt.ylabel('Page loading times (seconds)')
	plt.show()

def main():
	#bar()
	#cdf()
	#scatter()
	
if __name__ == "__main__":
    main()
