The files present in the folder :-


1) geo.py
-- Used to read the ufo_awesome.json file and geocode it to find the latitude and longitude of all the locations in the ufo_sightings.
-- Made use of pickle to store the geocoded data into chunks of 300 as the geopy api has a constraint of geocoding only a limited number of locations per API after which the program gives a timeout error.
-- For locations in countries outside the US, we have reverse geocoded them to get their respective regions
Libraries required
pip3 install json
pip3 install geopy
pip3 install csv
pip3 install pickle

2) combine_pickle_files.py
-- Used to combine the chunks of pickle files into a single pickle file

3) merge_and_cache.py
-- Used to merge the location and coordinates of the ufo_sightings and cache them using mongodb
Libraries required
pip3 install pymongo
Also make sure mongo is running on the terminal

4) NearDist.py

5) wiki_scifi.py
-- Used to scrape the Wikipedia page containing all the sci-fi movie lists released till date and stores it in a file named sci-fi_database.csv
Libraries required
pip install BeautifulSoup
pip install bs4
pip install urlib2

6) sci_fi.py
-- Used to combine the sci-fi_database.csv and the ufo_awesome sightings to produce the resultant sci_fi_output.tsv file with its 3 features.





7) compiled_list_1.pickle
This file contains following fields. ALl the names are pretty self evident.
m_possibility field is based on if the meteor distance is less than 100.
The file is a list of dictionaries. It can directly be connverted into json. as the field names with original file are consistent


{'sighted_at': '19950101',
'reported_at': '19950103', 
'location': ' Shelton, WA', 
'shape': '', 
'duration': '', 
'description': 'Telephoned Report:CA woman visiting daughter witness discs and triangular ships over Squaxin Island in Puget Sound. Dramatic.  Written report, with illustrations, submitted to NUFORC.', 
'latitude': 47.2150945, 
'longitude': -123.1007066, 
'Nearest Airport': 'Mason General Hospital Heliport', 
'Distance': 0.8555842771525585, 
'meteor_name': 'Hot Springs', 
'meteor_distance': 560.8548905304182, 
'm_possibility': 'False'}

Below are some properties of this file

a) Total entries:- 61067 (Same as ufo_sightings json)
b) Around 58k entries have their lat long value populated.
c) Out of these entries, 5.8k has m_possibility value as True

8)getYearWiseUFOCount.py
-- Used to just understand the no.of UFO sightings recorded or sighted in each year. 
-- This helped us to focus on the census data for the years where the highest sightings are reported (>400 ~ around 0.6 percentile of the total sightings) 

Libraries required
pip3 install json
pip3 install csv

9)UFO_Join_Census.py
-- joins UFO data with Census data (of 2000,2010) which covers timeperiod from 1991 to 2010. 
-- We group and count the UFO sightings by County and join this with the Census data
-- Output no.of sightings in a state, county and the year with the respective population density and housing density.

Libraries required
pip3 install json
pip3 install csv
