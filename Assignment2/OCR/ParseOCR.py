import csv
import re
from collections import defaultdict
import os
data = {}
dictkeys = ['Date of Sighting', 'Date of Report', 'Location', 'Shape', 'Duration', 'Description']


rootdir = 'OCR_Output'
regularExpressions = {}
regularExpressions['Date of Sighting_Duration'] = re.compile('Sighting = (.*)\n')
regularExpressions['DESCRIPTION'] = re.compile('DESCRIPTION = (.*)\n')
regularExpressions['Pos_OBSERVER_Loc'] = re.compile('OBSERVER = (.*)\n')
regularExpressions['HOW_Observed_Desc'] = re.compile('OBSERVED = (.*)\n')
regularExpressions['Direction_Desc'] = re.compile('OBSERVED = (.*)\n')
regularExpressions['AngleOfSight_Desc'] = re.compile('OBSERVED = (.*)\n')
regularExpressions['DISTANCE'] =  re.compile('OBSERVED = (.*)\n')
regularExpressions['MOVEMENTS'] =  re.compile('OBSERVED = (.*)\n')
regularExpressions['MET_Observed_Desc'] = re.compile('OBSERVED = (.*)\n')

keywords = ['sighting','description','pos_observer_loc','how_observed_Desc','direction_desc','angleofsight_desc','distance','movements','met_observed_desc']



#def matchLinewithRegex(line):

	# for k,v in regularExpressions.items():
	# 	output = v.match(line)
	# 	if output is  not None:
	# 		break
	# return output






def parse(filepath):
	with open(filepath, encoding='utf8') as file:
		content = file.read()
		if 'flying' in content.lower():
			lines = content.split('\n\n')
			#lines = filter(None, lines)
			lines = [line for line in lines if line != ' ']
			matchedKeyword = ''
			for line in lines:
				for keyword in keywords:
					if keyword in line:
						matchedKeyword =keyword
						break
				print(matchedKeyword)
				# if matched == True:
				# 	data = lines.next()
				# 	print(data)



				# if any (keyword in line for keyword in keywords):
				# 	keyword
				# 	matched = True
				# 	print(keyword)
				# if matched == True:
				# 	data = lines.next()
				# 	print(data)
				# 	continue





# for subdir, dirs, files in os.walk(rootdir):
# 	for file in files:
# 		print(file)
# 		break

ctr = 0
for subdir in os.listdir(rootdir):
	print('inside subdir')
	for files in os.walk(str(subdir)+'/outtxt/'):
		fileCountItr = len(files[2])+1
		for i in range(4,5):  #change back to 1 , fileCountItr
			parse(str(subdir)+'/outtxt/'+ str(i)+'.txt')
			i = i+1
			#ctr = ctr+1

print(ctr)

# class _RegExLib:
#     """Set up regular expressions"""
#     # use https://regexper.com to visualise these if required
#     _reg_school = re.compile('School = (.*)\n')
#     _reg_grade = re.compile('Grade = (.*)\n')
#     _reg_name_score = re.compile('(Name|Score)')
#
#     def __init__(self, line):
#         # check whether line has a positive match with all of the regular expressions
#         self.school = self._reg_school.match(line)
#         self.grade = self._reg_grade.match(line)
#         self.name_score = self._reg_name_score.search(line)



