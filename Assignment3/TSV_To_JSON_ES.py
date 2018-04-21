import json
from elasticsearch import Elasticsearch
import sys, json
import requests

index_name="bigdata"
es = Elasticsearch(['localhost:9200'])

count=0
with open('UFO_Awesome_V3.json', 'w') as output,open("ufo_awesome_FINAL_OUTPUT_v2.tsv",mode='r',encoding='ISO-8859-1') as tsv_in:
	next(tsv_in,None)
	for line in tsv_in:
		tempList = line.strip().replace('"','').split("\t")
		len_tempList = len(tempList)
		if len_tempList < 28:
			for i in range(len_tempList,28):
				tempList.append('')
		

		j = json.dumps({"sighted_at": tempList[0],"reported_at": tempList[1], "location": tempList[2].strip(),
										   "shape": tempList[3], "duration": tempList[4],  "description": tempList[5],
										   "latitude": tempList[6], "longitude": tempList[7],	"NearestAirport": tempList[8],
										   "Distance": tempList[9], "MeteorName": tempList[10], "Meteordistance": tempList[11],
										   "Meteor possibility": tempList[12],  "Number of sci_fi movies released": tempList[13], "Number of ufo sightings": tempList[14],
										   "Ratio of number of ufo sightings to number of movies released in that year": tempList[15],"Possibility of ufo_sighting being a dillusion after a sci-fi movie being released?": tempList[16], "County": tempList[17],
										   "Population Density": tempList[18], "Housing Denisty": tempList[19], "Rural?": tempList[20],
										   "Image Filename": tempList[21], "Object Recognized in image": tempList[22],   "Image Caption": tempList[23],
										   "NER_PERSON": tempList[24], "NER_LOCATION": tempList[25], "NER_ORGANIZATION": tempList[26],
										   "NER_DATE": tempList[27] })
		count=count+1
		res = es.index(index=index_name, doc_type='assignment3', id=count, body=j)