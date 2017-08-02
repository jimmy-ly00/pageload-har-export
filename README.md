# Page Load Testing
Automates page load testing with Firefox + Selenium IDE + har-export-trigger. Exports to HAR to view page timings and resource loading times.
Originally used to test websites against a mid-latency network.

Raw sampled HAR data also provided.

Note: It does not use page ready method as it is unreliable (especially for JavaScript rendered websites) because it sometimes does not wait for DOM completion
## Prerequisite
```
pip install haralyzer
```
**Optional** (for graph.py script, can be omitted):
```
pip install matplotlib (may require sudo apt-get install python-tk)
pip install numpy
```
## Environment
Linux and Firefox 54 (should work with 42+)

## Installation - Firefox and Selenium IDE setup
### Firefox
#### 1. about:debugging
Load temporary add-on: **harexporttrigger-0.5.0-beta.10.xpi** (currently no signed version by developer)
	
#### 2. about:config
use these settings:
````
extensions.netmonitor.har.contentAPIToken = "test"
extensions.netmonitor.har.enableAutomation = "true"
````
#### 3. (Optional) In Firefox Developer Tools (F12):
```settings > tick "disable HTTP Cache"```

### Selenium IDE
Download and install https://addons.mozilla.org/en-GB/firefox/addon/selenium-ide/ 


## How to use
1. Open Firefox with the above settings
2. Open Firefox Developer Tools and then visit a website for testing. Genereated HAR files are located at (usually) ```~/.mozilla/firefox/[user]/har/logs```
4. To automate using Selenium script:
    1. Go to about:addons and Selenium IDE "Preferences"
	  2. Under "Selenium Core Extensions", select **user-extension.js** as provided (make sure while.js is in the same directory)
    3. Go to ```Firefox > Tools > Selenium IDE ```
	  4. Right click "Add Test Case" and select the **selenium** file as provided
	  5. Run test case
5. Put **graph.py** script inside ~/.mozilla/firefox/[user]/har/logs folder and run ``` ./graph.py ```


## Resources
https://github.com/firebug/har-export-trigger

https://addons.mozilla.org/en-GB/firefox/addon/selenium-ide/

http://www.software-testing-tutorials-automation.com/2013/07/example-of-while-and-endwhile-loop.html
