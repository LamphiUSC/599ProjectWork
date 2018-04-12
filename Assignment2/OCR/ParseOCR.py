import csv
import re
from collections import defaultdict
import os
Outputdata = {}
dictkeys = ['Date of Sighting', 'Location', 'Shape', 'Duration', 'Description']
# we will have 'Date of Report' = Date of Sighting as we are unable to extract any field like date of reports
for k in dictkeys:
	Outputdata[k] = []


rootdir = 'OCR_Output'
regExpPatterns = {}
regExpPatterns['duration'] = re.compile('\d+\s*mins|\d+\s*secs|\d+\s*minutes|\d+\s*seconds')
regExpPatterns['date'] = re.compile(r'\d+\s*\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june|july|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s*\d+')
regExpPatterns['year'] = re.compile('\d+$') # to extract year datetime string
# regExpPatterns['Pos_OBSERVER_Loc'] = re.compile('OBSERVER = (.*)\n')
# regExpPatterns['HOW_Observed_Desc'] = re.compile('OBSERVED = (.*)\n')
# regExpPatterns['Direction_Desc'] = re.compile('OBSERVED = (.*)\n')
# regularExpressions['AngleOfSight_Desc'] = re.compile('OBSERVED = (.*)\n')
# regularExpressions['DISTANCE'] =  re.compile('OBSERVED = (.*)\n')
# regularExpressions['MOVEMENTS'] =  re.compile('OBSERVED = (.*)\n')
# regularExpressions['MET_Observed_Desc'] = re.compile('OBSERVED = (.*)\n')

keywords = ['sighting','description','location']
#'how_observed_Desc','direction_desc','angleofsight_desc','distance','movements','met_observed_desc'


def convert(dateString):
	# input like '26 jan 85' convert to 19850126
	months= {'jan':'01','feb':'02','mar':'03','apr':'04','may':'05','june':'06','july':'07','aug':'08','sep':'09','oct':'10','nov':'11','dec':'12'}
	for k in months.keys():
		if k in dateString:
			month = months[k]
			break

	year  =re.compile('\d+$').search(dateString).group()
	if len(year) ==2:
		year = '19'+ year
	res = year+month+dateString[:2]
	return res


def parse(filepath):
	with open(filepath, encoding='utf8') as file:
		content = file.read().lower()
		if 'flying' in content:
			lines = content.split('\n\n')
			#lines = filter(None, lines)
			lines = [line for line in lines if len(line) >=3]

			linesItr = 0
			ctrCheck = len(lines)-1
			tempCtr = 0
			while linesItr <= ctrCheck:
				#print('in loop' + lines[linesItr])
				matchedKeyword = ''
				for keyword in keywords:
					if keyword in lines[linesItr]:
						matchedKeyword =keyword
						break
				#print(matchedKeyword)
				if len(matchedKeyword) > 1:
					linesItr +=1 # to skip this data on the next line
					try:
						linedata = lines[linesItr]
					except:
						print ('issue in file '+ filepath)
						print(lines)
						print('Issue at lineITr no data at '+ linesItr)
					if matchedKeyword == 'sighting': # we extract date of sight and duration and date of report
						tempCtr+=1
						regexResult = regExpPatterns['duration'].search(linedata)
						if regexResult is not None:
							Outputdata['Duration'].append(regexResult.group())
						else:
							Outputdata['Duration'].append('')
						regexResult = regExpPatterns['date'].search(linedata)
						if regexResult is not None:
							Outputdata['Date of Sighting'].append(convert(regexResult.group()))
						else:
							Outputdata['Date of Sighting'].append('')
					elif matchedKeyword =='description':
						tempCtr+=1
						Outputdata['Description'].append(linedata)
					elif matchedKeyword == 'location':
						tempCtr+=1
						if '\n' in linedata:
							linedata =linedata.replace('\n', ' ')
						Outputdata['Location'].append(linedata)
				if tempCtr == len(keywords):
					break
				linesItr +=1



for subdir in os.listdir(rootdir):
	print('inside subdir')
	for files in os.walk(str(subdir)+'/outtxt/'):
		fileCountItr = len(files[2])+1
		for i in range(4,5):  #TO DO : change back to 1 , fileCountItr
			#print(str(subdir)+'/outtxt/'+ str(i)+'.txt')
			parse(str(subdir)+'/outtxt/'+ str(i)+'.txt')
			i = i+1

print(Outputdata)
tsvout=open('ufo_awesome_FINAL_OUTPUT.tsv', 'a')
tsvout.write('\n')
irtlen = len(Outputdata['Date of Sighting'])
for i in range(irtlen):
	tsvout.write(Outputdata['Date of Sighting'][i]+'\t'+ Outputdata['Date of Sighting'][i]+ \
				 '\t'+Outputdata['Location'][i]+ '\t'+ ''+ \
				 '\t'+ Outputdata['Duration'][i]+ '\t'+ Outputdata['Description'][i])
	tsvout.write('\n')