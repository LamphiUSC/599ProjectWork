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
-- Used to find the nearest airport to a geocoded location. We are storing all the unique locations in the Mongo DB
-- For US locations, we find nearest airport by assuming that it would be in either same state or in theneighbouring state. For US neighbouring state we are using the pickle file neighbour_dict.pickle
-- For non-US locations, we assume that the nearest airport will be in the same country.

5) wiki_scifi.py
-- Used to scrape the Wikipedia page containing all the sci-fi movie lists released till date and stores it in a file named sci-fi_database.csv
Libraries required
pip install BeautifulSoup
pip install bs4
pip install urlib2

6) sci_fi.py
-- Used to combine the sci-fi_database.csv and the ufo_awesome sightings to produce the resultant sci_fi_output.tsv file with its 3 features.


7) meteor.py
-- Use Meteorite_Landings.csv as the dataset. Index it based upon the year of the meteor landing.
-- Merge the unique locations stored in mongoDB to the UFO sighting Dataset.
-- Find the nearest meteor landings based on geocoded locations and the year.


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
