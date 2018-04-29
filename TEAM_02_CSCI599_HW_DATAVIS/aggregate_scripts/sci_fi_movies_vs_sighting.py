import csv

input_reader = open("../ufo_awesome_FINAL_OUTPUT_v2.tsv",'rU')
reader = csv.reader(input_reader, delimiter = '\t')

output = open("sci_fi_movies_vs_sighting.tsv",'w')
#Open the output file to store the aggregated tsv
output.write("Year\tNo of sightings\tNo of sci-fi movies released\n")

year_dict = {}
firstLine = True
for row in reader:
	if firstLine:
		firstLine = False
		continue
	if row[12] == "TRUE":
		year = row[0][:4]
		if year is "0":
			year = row[1][:4]
		scifi_count = row[13]
		sighting_count = row[14]
		if year not in year_dict:
			year_dict[year] = {}
			year_dict[year]["sci-fi"]=0
			year_dict[year]["sighting"]=0
		#check count of the sci-fi vs sighting
		year_dict[year]["sci-fi"]=scifi_count
		year_dict[year]["sighting"]=sighting_count
	
	#populate the TSV
for key in year_dict:
	if year_dict[key]["sci-fi"] !=0 or year_dict[key]["sighting"] != 0:
		print key, year_dict[key]
		output.write(str(key)+'\t'+str(year_dict[key]["sighting"])+'\t'+str(year_dict[key]["sci-fi"])+'\n')