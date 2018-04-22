import csv
import dateparser
import re
output = open("ShapeReported_year_count.tsv",'w')
output.write("Year\tOneD\tTwoD\tThreeDOrObject\tUnknown\n")
OneDShapes = ['light','flash', 'zigzag', 'diagonal']
TwoDShapes = ['ball', 'circular', 'disc', 'round', 'disk', 'diamond','rectangle', 'teardrop','oval' , 'disc','fireball','beachball']
ThreeDOrObjectShapes = ['egg','dome','pyramid','cigar','cylinder','sphere','humanoid','10 pence']



# round like  etc..
# oval , disc, egg, teardrop
# Cylinder : cigar ,cylinder, dome , diagonal , pyramid
# Light : light, flash
#weird shapes like 'humanoid', milk bottle, ''10 PENCE''
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



		if year not  in yearDict.keys():
			yearDict[year] = {}
			yearDict[year]["1D"] = 0
			yearDict[year]["2D"] = 0
			yearDict[year]["3DOrObject"] = 0
			yearDict[year]["Unknown"] = 0

		shape = r[3].strip().lower()  # r[3] shape column

		if shape != '':
			if shape == 'unknown' or shape == 'other':
				yearDict[year]["Unknown"] = yearDict[year]["Unknown"] +1
			else:
				shapeWords = re.split(regexSplit, shape)
		else:
			# if the shape column is empty , look for shape in description which is r[5]
			shapeWords = re.split(regexSplit, r[5].lower())  # 'description' r[5]

		if ('light' or 'flash' or 'zigzag' or 'diagonal') in shapeWords:
			yearDict[year]["1D"] = yearDict[year]["1D"] + 1
		elif ('ball' or 'circular' or 'disc' or 'round' or 'disk' or 'diamond' or 'rectangle' or 'teardrop' or 'oval' or 'disc' or 'fireball' or 'beachball') in shapeWords:
			yearDict[year]["2D"] = yearDict[year]["2D"] + 1
		elif ('egg' or 'dome' or 'pyramid' or 'cigar' or 'cylinder' or 'sphere' or 'humanoid' or '10 pence') in shapeWords:
			yearDict[year]["3DOrObject"] = yearDict[year]["3DOrObject"] + 1




for k in yearDict.keys():
	if yearDict[k]["1D"] != 0 or yearDict[k]["2D"] != 0 or  yearDict[k]["3DOrObject"] != 0 or yearDict[k]["Unknown"] != 0:
		output.write(str(k) + '\t' + str(yearDict[k]["1D"]) + '\t' + str(yearDict[k]["2D"]) + '\t' + str(yearDict[k]["3DOrObject"]) + '\t' + str(yearDict[k]["Unknown"])+'\n')


