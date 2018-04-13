import csv
import re
from collections import defaultdict
from autocorrect import spell
import enchant
import os


Result = []


rootdir = 'OCR_Output'
regExpPatterns = {}
regExpPatterns['duration'] = re.compile('(\d+[a-z]+)\s*mins|(\d+[a-z]+)\s*minute|\d+\s*se[a-z]*|\d+\s*secs|\d+\s*minutes|\d+\s*seconds|\d+\s*h[a-z]*rs|still there')
regExpPatterns['date'] = re.compile(r'\d+\s*\b(?:jan(?:uary)?|feb(?:ruary)?|mar(?:ch)?|apr(?:il)?|may|june|july|aug(?:ust)?|sep(?:tember)?|oct(?:ober)?|nov(?:ember)?|dec(?:ember)?)\s*\d+')
regExpPatterns['year'] = re.compile('\d+$') # to extract year datetime string
regExpPatterns['DescQuestionnaire'] = re.compile('number of|object|size|shape|colour')
regExpPatterns['LocQuestionnaire'] = re.compile('pos[a-z]*\s*|of\s*[a-z]*observer[a-z]*|[a-z]*mov[a-z]*|[a-z]*loc(.*)door(.*)|stat[a-z]*')
regExpPatterns['SightingQuestionnaire'] = re.compile('[a-z]*local\s*[a-z]*\s*[a-z]*[0-9]*\s*[a-z]*\s*(quoted|quetedb)')
# regExpPatterns['Pos_OBSERVER_Loc'] = re.compile('OBSERVER = (.*)\n')
# regExpPatterns['HOW_Observed_Desc'] = re.compile('OBSERVED = (.*)\n')
# regExpPatterns['Direction_Desc'] = re.compile('OBSERVED = (.*)\n')
# regularExpressions['AngleOfSight_Desc'] = re.compile('OBSERVED = (.*)\n')
# regularExpressions['DISTANCE'] =  re.compile('OBSERVED = (.*)\n')
# regularExpressions['MOVEMENTS'] =  re.compile('OBSERVED = (.*)\n')
# regularExpressions['MET_Observed_Desc'] = re.compile('OBSERVED = (.*)\n')

keywords = {}
keywords['sighting']= re.compile('sighting(.*)description',re.DOTALL)
keywords['description'] = re.compile('description(.*)exact',re.DOTALL)
keywords['location'] = re.compile('exact pos(.*)ow observed',re.DOTALL)
possibleShapes =['10 PENCE','cigar','cylinder','light','ball','round','circular','flash','dome','pyramid','diagonal','sphere']
#'how_observed_Desc','direction_desc','angleofsight_desc','distance','movements','met_observed_desc'


def convert(dateString):
	# input like '26 jan 85' convert to 19850126
	months= {'jan':'01','feb':'02','mar':'03','apr':'04','may':'05','june':'06','july':'07','aug':'08','sept':'09','oct':'10','nov':'11','dec':'12'}
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
	duration =''
	date_of_sight= ''
	location =''
	desc =''
	shape =''

	with open(filepath, encoding='utf8') as file:
		content = file.read().lower()
		lines = content.split('\n')
		lines = [line for line in lines if len(line.strip()) >= 3]
		content = ''.join(lines)
		tempCtr = 0
		if 'flying' in content:  #  or 'aerial' or 'ministry'
			#print(filepath)
			for keyword, keywordRegex in keywords.items():
				reqData=''
				regexSearchRes = keywordRegex.search(content)
				if regexSearchRes:
					for r in  regexSearchRes.groups():
						reqData += r
				reqData =  re.sub('[^A-Z\sa-z0-9]+', '',reqData) # remove non digit non alphabet chars
				if reqData: #extract fields
					if keyword == 'sighting':  # we extract date of sight and duration and date of report
						tempCtr += 1
						reqData = regExpPatterns['SightingQuestionnaire'].sub('',reqData.strip()) # remove questionnarie desc from text ss
						regexResult = regExpPatterns['duration'].search(reqData)
						if regexResult is not None:
							duration = regexResult.group()
							reqData =  regExpPatterns['duration'].sub('',reqData)
						regexResult = regExpPatterns['date'].search(reqData)
						if regexResult is not None:
							date_of_sight = convert(regexResult.group())
						else:
							date_of_sight = reqData
					elif keyword == 'description':
						tempCtr += 1
						desc = regExpPatterns['DescQuestionnaire'].sub('',reqData)
						for s in possibleShapes:
							if s in desc:
								shape +=s+','
						# TO DO : get shape also
					elif keyword == 'location':
						tempCtr += 1
						if '\n' in reqData:
							reqData = reqData.replace('\n', ' ').strip()
						#reqData.replace( regExpPatterns['LocQuestionnaire'].group(),'',1)
						location = regExpPatterns['LocQuestionnaire'].sub('',reqData)
						#location.replace('moving','', 1)
			if tempCtr > 1: # (>1)s
				Result.append( filepath+'\t' +date_of_sight + '\t' + date_of_sight + '\t' + location +  '\t'  + shape + '\t'  + duration +  '\t'  + desc)
			# else:
			# 	print(filepath)







			# print ('file in process '+filepath)
			#
			# lines = content.split('\n')
			# #lines = filter(None, lines)
			# lines = [line for line in lines if len(line.strip()) >=3]
			#
			# linesItr = 0
			# ctrCheck = len(lines)-1
			# tempCtr = 0
			# while linesItr <= ctrCheck:
			# 	#print('in loop' + lines[linesItr])
			# 	matchedKeyword = ''
			# 	for keyword, keywordRegex in keywords.items():
			# 		if keywordRegex.search(lines[linesItr]):
			# 			matchedKeyword = keyword
			# 			break
			#
			#
			# 	#print(matchedKeyword)
			# 	if len(matchedKeyword) > 1:
			# 		linesItr +=1 # to skip this data on the next line
			# 		try:
			# 			linedata = lines[linesItr]
			# 		except:
			# 			print ('issue in file '+ filepath)
			# 			print(lines)
			# 			print('Issue at lineITr no data at '+ str(linesItr))
			# 		if matchedKeyword == 'sighting': # we extract date of sight and duration and date of report
			# 			tempCtr+=1
			# 			regexResult = regExpPatterns['duration'].search(linedata)
			# 			if regexResult is not None:
			# 				duration = regexResult.group()
			# 			regexResult = regExpPatterns['date'].search(linedata)
			# 			if regexResult is not None:
			# 				date_of_sight = convert(regexResult.group())
			# 			else:
			# 				date_of_sight= linedata
			# 		elif matchedKeyword =='description':
			# 			tempCtr+=1
			# 			desc=linedata
			# 		elif matchedKeyword == 'location':
			# 			tempCtr+=1
			# 			if '\n' in linedata:
			# 				linedata =linedata.replace('\n', ' ').strip()
			# 			location = linedata
			# 	if tempCtr == len(keywords):
			# 		Result.append(date_of_sight + '  ' + date_of_sight + '  ' + location + '  ' + 'N/A' + '  ' + duration + '  ' + desc)
			# 		break
			# 	linesItr +=1
	#Result.append(date_of_sight+'\t'+ date_of_sight+ '\t'+location+ '\t'+ ''+ '\t'+duration+'\t'+ desc




for subdir in os.listdir(rootdir):
	#print('inside subdir '+ subdir)
	for files in os.walk(rootdir + '/' + str(subdir) + '/outtxt'):
		fileCountItr = len(files[2])+1
		for i in range(1,fileCountItr):  #TO DO : change back to 1 , fileCountItr
			#print(str(subdir)+'/outtxt/'+ str(i)+'.txt')
			parse(rootdir + '/'+str(subdir)+'/outtxt/'+ str(i)+'.txt')
			i = i+1

#print(Result)
# print(len(Result))
# for res in Result:
# 	print(res)

tsvout=open('tempOutput.tsv', 'w')
for res in Result:
	tsvout.write(res)
	tsvout.write('\n')


# 	print(Outputdata['Date of Sighting'][i]+'\t'+ Outputdata['Date of Sighting'][i]+ \
# 				 '\t'+Outputdata['Location'][i]+ '\t'+ ''+ \
#  				 '\t'+ Outputdata['Duration'][i]+ '\t'+ Outputdata['Description'][i])
# 	tsvout.write('\n')