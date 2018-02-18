from geopy.geocoders import Nominatim
geolocator = Nominatim()
import csv
from collections import defaultdict
from geopy.distance import vincenty
import json

airport_db = open('airport.csv', "r")
airport = csv.reader(airport_db)

state_code = open('state_code.csv', "r")
state = csv.reader(state_code)

state_set = set() #set containing the 2 letter state codes in US
for row in state:
    state_code = row[0].split(",")[1].replace("\"","").lower()
    state_set.add(state_code)

ufo_data = open('ufo_awesome.tsv', "r")
ufo = csv.reader(ufo_data, delimiter='\t')

ufo_cities = set() #all the unique cities, state in the ufo data set in US only
for row in ufo:
        city = row[2].strip().lower()
        if city not in ufo_cities and len(city.split(','))==2 and city.split(',')[1].strip() in state_set:
            ufo_cities.add(city)

ufo_city_dist_closest_airport_dict = {}

for ufo_city in ufo_cities:
    geocoder_ufo = geolocator.geocode(ufo_city)
    location2 = (geocoder_ufo.latitude, geocoder_ufo.longitude)
    min_dist = 999999999
    airport_nm = ""
    for row in airport:
        if row[1]:
            try:
                if row[1] == 'FAA':
                    continue
                airport_name = row[1]+" Airport, US"
                geocoder_airport = geolocator.geocode(airport_name)
                location1 = (geocoder_airport.latitude, geocoder_airport.longitude)
                distance = vincenty(location1, location2).miles
                if distance < min_dist:
                    min_dist = distance
                    airport_nm = row[4]
                print str(distance)+" "+str(min_dist)
            except:
                pass
    ufo_city_dist_closest_airport_dict[ufo_city] = [min_dist,airport_nm]
    break

print ufo_city_dist_closest_airport_dict
