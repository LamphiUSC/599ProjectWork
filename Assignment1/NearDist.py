import csv
from time import sleep
from collections import defaultdict
from geopy.distance import vincenty
import pickle

from pymongo import MongoClient

db = MongoClient().ufo.cities

airport_fname = "airport_data.pickle"
us_neighbor_fname = "neighbour_dict.pickle"

# Now load airport dictionary and US neighbouring states dictionary
with open(airport_fname, 'rb') as f:
    airport_data = pickle.load(f)
with open(us_neighbor_fname, 'rb') as f:
    us_neighbour_data = pickle.load(f)
print(type(airport_data),len(airport_data))
print(type(us_neighbour_data),len(us_neighbour_data))

def generateAirportList(region_list):
    #print("In generateAirportList")
    airport_list = []
    for region in region_list:
        airport_list = airport_list + airport_data[region]
    return airport_list

def findNearest(city,region_list):
    #print("In findNearest",str(city))
    airport_list = generateAirportList(region_list)
    #print(city,type(city))
    city_lat_lon = (float(city['latitude']),float(city['longitude']))
    #print(city_lat_lon)
    min_dist = None
    airport_name = None
    for airport in airport_list:

        #print("Checking for airport:- ",airport)
        airport_lat_lon = (airport[1],airport[2])
        #print(airport_lat_lon)
        vin_dist = vincenty(city_lat_lon, airport_lat_lon).miles
        if min_dist is None:
            min_dist = vin_dist
            airport_name = airport[0]
        else:
            if vin_dist < min_dist:
                min_dist = vin_dist
                airport_name= airport[0]
    return airport_name,min_dist

# sanity checks
# Iterate over each city to get the nearest airport
# Assumption:- For the US sightings we assume that the nearest airport will be in
count = 0

for row in db.find():
    if count%100 == 0:
        print(count)
    count=count+1
    region = row['region']
    if region == "US":
        # check for all US regions.
        region_list = us_neighbour_data.keys()
        airport_name, dist = findNearest(row, region_list)
    elif region[:2] == "US":
        # This loop is for all the US states
        region_list = us_neighbour_data[region]
        region_list.append(region)
        airport_name,dist = findNearest(row,region_list)
    else:
        # This loop is for Non US regions
        region_list = [region]
        airport_name, dist = findNearest(row, region_list)
    #print(airport_name,dist)
    count = count+1
    db.update_one({'_id':row['_id']},{"$set":{'Nearest Airport':airport_name,'Distance':dist}})
