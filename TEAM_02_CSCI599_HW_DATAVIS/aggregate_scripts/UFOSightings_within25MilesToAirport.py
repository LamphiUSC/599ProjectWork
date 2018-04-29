import csv
import dateparser
output = open("Within_25Miles_Otherwise_year_count.tsv",'w')
output.write("Year\tWithin_25Miles\tOutside_25Miles\n")

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
        if len(r[9].strip()) <= 0:
            continue
        distance = float(r[9].strip())
        if year not  in yearDict.keys():
            yearDict[year] = {}
            yearDict[year]["Within_25Miles"] = 0
            yearDict[year]["Outside_25Miles"] = 0
        if distance <= 25:
            #checking for distance
            yearDict[year]["Within_25Miles"] = yearDict[year]["Within_25Miles"] + 1
        else:
            yearDict[year]["Outside_25Miles"] = yearDict[year]["Outside_25Miles"] + 1

for k in yearDict.keys():
    if yearDict[k]["Within_25Miles"] != 0 or yearDict[k]["Outside_25Miles"] != 0:
        output.write(str(k) + '\t' + str(yearDict[k]["Within_25Miles"]) + '\t' + str(yearDict[k]["Outside_25Miles"]) + '\n')


