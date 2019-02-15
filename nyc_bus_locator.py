"""
This script will output the current latitude and longitude for each bus along
a particular line and print the results in the console.

To run this script you'll need an API key from the MTA, which you can register
for here: https://datamine.mta.info/user/register. Once you have the key,
you can run the script with:

python <MTA_KEY> <BUS_LINE>

Note that any letters in the bus line should be capitalized.
"""

from __future__ import print_function
import json
try:
    import urllib2 as urllib
except ImportError:
    import urllib.request as urllib
import os
import sys

# Check to make sure name of python script, API key, and bus line are entered
if not len(sys.argv) == 3:
    print ("Invalid number of arguments. Run as: python <MTA_KEY> <BUS_LINE>")
    sys.exit()

bus = sys.argv[2]

# Retrieving URL
url = "http://bustime.mta.info/api/siri/vehicle-monitoring.json?key=" + \
    sys.argv[1] + "&VehicleMonitoringDetailLevel=calls&LineRef=" + bus

# Open and load data from the JSON
response = urllib.urlopen(url)
busdata = response.read().decode("utf-8")
busdata = json.loads(busdata)

# Filter the total bus data down to the data for each bus that's
# currrently running
filteredbusdata = busdata['Siri']['ServiceDelivery'] \
    ['VehicleMonitoringDelivery'][0]['VehicleActivity']

# Query the total number of buses running
busnum = len(filteredbusdata)

# Print an extra space just for ease of reading
print("")

# Print the bus line and number of buses
print("Bus line : " + str(bus))
print("Number of active buses : " + str(busnum))

# Then find and print the lat and long for each bus that's running
for i in range(busnum):
    lat = filteredbusdata[i]['MonitoredVehicleJourney'] \
        ['VehicleLocation']['Latitude']
    long = filteredbusdata[i]['MonitoredVehicleJourney'] \
        ['VehicleLocation']['Longitude']
    print("Bus " + str(i) + " is at latitude " + str(lat) + " and longitude " \
        + str(long))

# Print an extra space just for ease of reading
print("")
