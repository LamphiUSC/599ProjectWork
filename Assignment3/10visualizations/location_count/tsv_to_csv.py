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
with open("location_aggregation_cloud.tsv","r", encoding = "ISO-8859-1") as f:
    for line in f:
       if count == 1:
           count = count + 1
           continue
       sp=line.split("\t")

       if len(sp) < 3:
           continue
       # print(len(sp))
       if not sp[1]:
           # data.setdefault("data",[]).append({"state": sp[0], "sightings": int(sp[2].strip())})
           continue
       else:
           data.setdefault("data", []).append({"state": sp[1], "sightings": int(sp[2].strip())})


f = csv.writer(open("location_aggregation_cloud.csv", "w"))

f.writerow(["id", "value"])
for x in range(0,len(data["data"])):
    print(data["data"][x])
    f.writerow([data["data"][x]["state"],
                data["data"][x]["sightings"]])

