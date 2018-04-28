import csv

input_reader = open("../ufo_awesome_FINAL_OUTPUT_v2.tsv",'rU')
reader = csv.reader(input_reader, delimiter = '\t')

#Open the output file to store the aggregated tsv
output = open("rural_vs_urban_year_count.tsv",'w')

output.write("Year\tNo of sighting in Rural\tNo of sighting in Urban\n")

year_dict = {}
firstLine = True
for row in reader:
	if firstLine:
		firstLine = False
		continue
	year = row[0][:4]
	if year is "0":
		year = row[1][:4]
	isRural = row[20]
	if year not in year_dict:
		year_dict[year] = {}
		year_dict[year]["Rural"]=0
		year_dict[year]["Urban"]=0
	#check if the sighting took place in rural or urban area
	if isRural=="TRUE":
		year_dict[year]["Rural"]=year_dict[year]["Rural"]+1
	elif isRural=="FALSE":
		year_dict[year]["Urban"]=year_dict[year]["Urban"]+1

#populate the TSV
for key in year_dict:
	if year_dict[key]["Rural"] !=0 or year_dict[key]["Urban"] != 0:
		print key, year_dict[key]
		output.write(str(key)+'\t'+str(year_dict[key]["Rural"])+'\t'+str(year_dict[key]["Urban"])+'\n')


	

	