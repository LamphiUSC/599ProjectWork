import json
import csv

data={}
count = 1

# tsv to csv
fcsv = csv.writer(open("No_of_UFO_Sightings_per_year.csv", "w"))
fcsv.writerow(["Year", "No_of_UFO_Sightings"])
with open("UFOSightings_year_count.tsv","r", encoding = "ISO-8859-1") as f:
    for line in f:
       if count == 1:
           count = count + 1
           continue
       sp=line.split("\t")

       if len(sp) < 2:
           continue
       # print(len(sp))
       csvList = []
       for i in range(0,len(sp)):
           csvList.append(sp[i].strip())
       fcsv.writerow(csvList)
