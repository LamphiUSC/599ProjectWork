# import sys
# import string
# import common
#
# # file_ob = open("599ProjectWork/Assignment3/aggregate_scripts/location_aggregation_cloud.tsv","r")
# # string = file_ob.readlines()
#
# titles = [string.strip(t) for t in string.split(sys.stdin.readline(), sep="\t")]
# for l in sys.stdin:
#     d = {}
#     for t, f in zip(titles, string.split(l, sep="\t")):
#         d[t] = f
#     print(common.json.dumps(d, indent=4))




import json
import csv

data={}
count = 1
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


    # json.dump(data, outfile)

# print(data)


