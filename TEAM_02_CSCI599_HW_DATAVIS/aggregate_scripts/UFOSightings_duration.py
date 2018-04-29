import csv
import dateparser
output = open("duration_year_count.tsv",'w')
output.write("Year\tSecs\tMinutes\tHours\tDays\tNoDuration\n")

# aggregating based on duration like within secs, minutes, weird text like still there etc..
resultDict = {} # key is year : per year how many sightings within secs, minutes, still there or no duration mentioned etc..
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
		duration = r[4].strip().lower()
		if year not  in resultDict.keys():
			resultDict[year] = {}
			resultDict[year]["Secs"] = 0
			resultDict[year]["Minutes"] = 0
			resultDict[year]["Hours"] =0
			resultDict[year]["Days"] = 0
			resultDict[year]["NoDuration"] = 0
		if len(duration) == 0:
			resultDict[year]["NoDuration"] = resultDict[year]["NoDuration"] + 1
		elif  ('sec' or 'secs' or 'second' or'seconds')  in duration:
			tempList = [int(s) for s in duration.split() if s.isdigit()]
			if len(tempList) >0:   # handling cases where duration is 90 secs which is technically 1.5 min
				if tempList[0] > 60:
					resultDict[year]["Minutes"] = resultDict[year]["Minutes"] + 1
			else:
				resultDict[year]["Secs"] = resultDict[year]["Secs"] + 1
		elif ('min' or 'mins' or 'minutes' or 'minutes') in duration :
			tempList = [int(s) for s in duration.split() if s.isdigit()]
			# handling cases where duration is 90 minutes which 1.5 hour
			if len(tempList) >0:
				if tempList[0] > 60:
					resultDict[year]["Hours"] = resultDict[year]["Hours"] + 1
			else:
				resultDict[year]["Minutes"] = resultDict[year]["Minutes"] + 1

		elif ('hr' or 'hrs' or 'hour' or 'hours') in duration:
			resultDict[year]["Hours"] = resultDict[year]["Hours"] + 1
		elif ('day' or 'days') in duration:
			resultDict[year]["Days"] = resultDict[year]["Days"] + 1

for k in resultDict.keys():
	output.write(str(k) + '\t' + str(resultDict[k]["Secs"]) + '\t' + str(resultDict[k]["Minutes"]) + '\t' + str(resultDict[k]["Hours"]) + '\t' + str(resultDict[k]["Days"]) + '\t' + str(resultDict[k]["NoDuration"]) + '\n')



