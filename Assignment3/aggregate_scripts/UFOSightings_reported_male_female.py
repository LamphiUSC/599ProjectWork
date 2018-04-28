import csv
import dateparser
import re
output = open("ReportedBy_Male_Female_Adult_kid_year_count.tsv",'w')
output.write("Year\tMale\tFemale\tAdult\tNot_Adult\n")
regexSplit = re.compile(r'[`\-=~!@#$%^&* ()_+\[\]{};\'\\:"|<,./<>?]')

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
		if len(r[18].strip()) <= 0:  # 'population density'
			continue
		descriptionWords = re.split(regexSplit,r[5].lower())   # 'description' r[5]

		#check for keywords to find if male/female/adult/youth
		if year not  in yearDict.keys():
			yearDict[year] = {}
			yearDict[year]["Male"] = 0
			yearDict[year]["Female"] = 0
			yearDict[year]["Adult"] = 0
			yearDict[year]["Not_Adult"] = 0
		if ('he' or 'his' or 'man' or 'father' or 'men' or 'husband' or 'male' or 'couple' or 'family' ) in descriptionWords:
			yearDict[year]["Male"] = yearDict[year]["Male"] + 1
			yearDict[year]["Adult"] = yearDict[year]["Adult"] + 1
		elif ('woman' or 'female' or 'wife' or 'mother' or 'women' or 'girlfriend' or 'couple' or 'family' ) in descriptionWords:
			yearDict[year]["Female"] = yearDict[year]["Female"] + 1
			yearDict[year]["Adult"] = yearDict[year]["Adult"] + 1
		elif ('adult' or 'passenger' or 'dentist' or  'officer' or 'empl' or 'officers' or 'artist' or 'reporter' or 'individual' or 'caller') in descriptionWords:
			yearDict[year]["Adult"] = yearDict[year]["Adult"] + 1
		elif ('boy' or 'son' or 'girl' or 'daughter' or 'grandson' or 'children' or 'boys' or 'kids' or 'teen' or 'youth' or 'young') in descriptionWords:
			yearDict[year]["Not_Adult"] = yearDict[year]["Not_Adult"] + 1


#populate the TSV
for k in yearDict.keys():
	if yearDict[k]["Male"] != 0 or yearDict[k]["Female"] != 0:
		output.write(str(k) + '\t' + str(yearDict[k]["Male"]) + '\t' + str(yearDict[k]["Female"]) + '\t' + str(yearDict[k]["Adult"]) + '\t' + str(yearDict[k]["Not_Adult"])+'\n')


