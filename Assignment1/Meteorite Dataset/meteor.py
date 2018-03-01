#This code saves the meteor landings dataset intoa diectionary indexed by the year of landing
import csv
import json
import  pickle
from pymongo import MongoClient

meteorite_fname = "Meteorite_Landings.csv"

metorites_db = open(meteorite_fname, "r",encoding="UTF-8")
meteorites = csv.reader(metorites_db)

meteor_dict = {}

count=0
for row in meteorites:
    #print(row)
    if count == 0:
        count+=1
        #Ignore the first row as itcontains field names
        continue
    else:
        if row[6] !="" and row[7]!="" and row[8]!="":
            #Get the yearof meteor landing
            name = row[0]
            year_list = row[6].split("/")
            year = int(year_list[2][:4])
            try:
                lat = float(row[7])
                long = float(row[8])
            except ValueError as e:
                print(row[7],row[8])
            if lat!=0 and long != 0:
                record = [name,lat,long]
                if year in meteor_dict:
                    meteor_dict[year].append(record)
                else:
                    meteor_dict[year] = [record]
    count+=1

with open("meteorite_data.pickle",'wb') as f:
    pickle.dump(meteor_dict,f)

#Reload the json for UFO sightings
with open('ufo_awesome.json',encoding="utf8") as json_data:
    ufo_data = json.load(json_data)
    print(len(ufo_data))
    print(ufo_data[0],type(ufo_data[0]))

db = MongoClient().ufo.cities
ufo_cities_dict = {}

#Merge the uniquelocationstrings latitudde with the UFO sightings dataset.

count=0
for row in db.find():
    count+=1
    del row['_id']
    del row['region']
    if 'state' in row:
        del row['state']
    if 'country' in row:
        del row['country']
    location = row.pop('location')
    ufo_cities_dict[location] = row

compiled_list=[]
#This list willhave following structure
#{'sighted_at': '19951009',
# 'reported_at': '19951009',
# 'location': ' Iowa City, IA',
# 'shape': '',
# 'duration': '',
# 'description': 'Man repts. witnessing &quot;flash, followed by a classic UFO, w/ a tailfin at back.&quot; Red color on top half of tailfin. Became triangular.',
# 'latitude': 41.6612561,
# 'longitude': -91.5299106,
# 'Nearest Airport': 'University of Iowa Hospitals & Clinic Heliport',
# 'Distance': 0.9246877620849214}

for row in ufo_data:
    if row['location'] in ufo_cities_dict:
        row.update(ufo_cities_dict[row['location']])
    compiled_list.append(row)

#Save the list to  filesystem
with open("compiled_list.pickle",'wb') as f:
    pickle.dump(compiled_list,f)

#Now lets calculate if the meteor sighting is related to the UFO sightings.
from geopy.distance import vincenty
# This functionwillfind returnthe nearest meteorsighting relatedto the UFO sighting index by year.
def find_nearest_meteor(row,meteor_list):
    city_lat_lon = (float(row['latitude']),float(row['longitude']))
    min_dist = None
    for meteor in meteor_list:
        meteor_lat_lon = (meteor[1],meteor[2])
        #print(airport_lat_lon)
        try:
            vin_dist = vincenty(city_lat_lon, meteor_lat_lon).miles
        except ValueError as e:
            print(city_lat_lon,meteor_lat_lon)
        if min_dist is None:
            min_dist = vin_dist
            meteor_name = meteor[0]
        else:
            if vin_dist < min_dist:
                min_dist = vin_dist
                meteor_name= meteor[0]
    return meteor_name,min_dist
f_compiled_list = []
meteor_present = True
lat_lon_present=True
count_no_lat_long = 0
count_no_meteor_list= 0
count=0

for row in compiled_list:
    #count+=1
    mname_dict = {}
    if 'latitude' in row:
        meteor_present = True
        lat_lon_present=True
        #get the year
        if row['sighted_at'] != 0:
            year = int(row['sighted_at'][:4])
        else:
            year = int(row['reported_at'][:4])
        if year not in meteor_dict:
            meteor_present = False
            count_no_meteor_list+=1
        else:
            meteor_list = meteor_dict[year]
        if meteor_present:
            meteor_name,meteor_dist = find_nearest_meteor(row,meteor_list)
            #print(meteor_name,meteor_dist)
            mname_dict['meteor_name'] = meteor_name
            mname_dict['meteor_distance'] = meteor_dist
            if meteor_dist <=100:
                mname_dict['m_possibility'] = "True"
                count+=1
            else:
                mname_dict['m_possibility'] = 'False'
            row.update(mname_dict)
    else:
        lat_lon_present=False
        count_no_lat_long+=1
    f_compiled_list.append(row)
print(count)
#Save the final list to file
with open("compiled_list_1.pickle",'wb') as f:
    pickle.dump(f_compiled_list,f)
# This new list will have following structure
#{'sighted_at': '19950101',
#'reported_at': '19950103',
#'location': ' Shelton, WA',
#'shape': '',
#'duration': '',
#'description': 'Telephoned Report:CA woman visiting daughter witness discs and triangular ships over Squaxin Island in Puget Sound. Dramatic.  Written report, with illustrations, submitted to NUFORC.',
#'latitude': 47.2150945,
#'longitude': -123.1007066,
#'Nearest Airport': 'Mason General Hospital Heliport',
#'Distance': 0.8555842771525585,
#'meteor_name': 'Hot Springs',
#'meteor_distance': 560.8548905304182,
#'m_possibility': 'False'}