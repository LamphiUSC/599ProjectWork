import csv
import dateparser
output = open("UFOSightings_year_count.tsv",'w')
output.write("Year\tNo of UFO Sightings\n")

yearDict = {}
#test = int(ufo_data[0]['sighted_at'][0:4])
#print (type(test))
# read the ocr tsv file
with open("../ufo_awesome_FINAL_OUTPUT_v2.tsv",mode='r',encoding='ISO-8859-1') as ocr_tsv:
    tsvreader = csv.reader(ocr_tsv, delimiter='\t')
    next(tsvreader, None) # skip header
    for r in tsvreader:
        if len(r[0].strip()) <=0 or len(r[1].strip()) <=0:
            continue
        try:
            year = int(r[0][0:4]) #'sighted_at'
        except:
            year = dateparser.parse(r[0]).year
        if year == 0:
            try:
                year = int(r[1][0:4]) #'reported_at'
            except:
                year = dateparser.parse(r[1]).year
        if year in yearDict.keys():
            yearDict[year] = yearDict[year] + 1
        else:
            yearDict[year] = 1

#populate tsv
for k, v in yearDict.items():
    output.write(str(k)+'\t'+str(v)+'\n')

