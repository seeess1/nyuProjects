"""
This script will output the location and status for each bus along a
particular line and save the results in a csv file.

To run this script you'll need an API key from the MTA, which you can register
for here: https://datamine.mta.info/user/register. Once you have the key,
you can run the script with:

python <MTA_KEY> <BUS_LINE> <NAME_OF_CSV_FILE.csv>

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
import csv

"""
%pylab inline
pl.rc('font', size=15)
"""

# Check to make sure name of python script, API key, and bus line are entered
if not len(sys.argv) == 4:
    print ("Invalid number of arguments. Run as: python <MTA_KEY> <BUS_LINE> \
    <NAME_OF_CSV_FILE.csv>")
    sys.exit()

# Get the bus number
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

# Total number of buses running
busnum = len(filteredbusdata)

# Find the lat, long, name of the next stop, and distance to that stop for
# each bus on the line queried.

with open(sys.argv[3], 'w', newline='') as csvfile:
    fieldnames = ['Latitude','Longitude','Stop Name','Stop Status']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(busnum):
        lat = filteredbusdata[i]['MonitoredVehicleJourney'] \
            ['VehicleLocation']['Latitude']
        long = filteredbusdata[i]['MonitoredVehicleJourney'] \
            ['VehicleLocation']['Longitude']
        stname = filteredbusdata[i]['MonitoredVehicleJourney']['MonitoredCall']\
            ['StopPointName']
        ststat = filteredbusdata[i]['MonitoredVehicleJourney']['MonitoredCall']\
            ['Extensions']['Distances']['PresentableDistance']
        writer.writerow({'Latitude':lat,'Longitude':long,'Stop Name':stname,\
        'Stop Status':ststat})
