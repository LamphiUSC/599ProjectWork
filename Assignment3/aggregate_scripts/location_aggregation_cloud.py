import csv

input_reader = open("../ufo_awesome_FINAL_OUTPUT_v2.tsv",'rU')
reader = csv.reader(input_reader, delimiter = '\t')

output = open("location_aggregation_cloud.tsv",'w')

output.write("Country\tState\tNo of UFO sightings\n")

us_state_dict={}
country_dict = {}
firstLine = True
row_count = -1
for row in reader:
	row_count = row_count + 1
	if firstLine or row_count > 61067:
		firstLine = False
		continue
	location = row[2].strip().rstrip(',').upper()
	if "," in location and len(location.split(',')[-1].strip()) <= 3:
		state = location.split(',')[-1].strip()
		if state not in us_state_dict:
			us_state_dict[state]=0
		us_state_dict[state]=us_state_dict[state]+1
	else:
		country = location.strip()
		if ")" in country: 
			country=country[country.rfind("(")+1:country.rfind(")")]
		if country not in country_dict:
			country_dict[country]=0
		country_dict[country]=country_dict[country]+1

print country_dict

for key in us_state_dict:
	output.write("US\t"+key+"\t"+str(us_state_dict[key])+"\n")
for key in country_dict:
	output.write(key+"\t\t"+str(country_dict[key])+"\n")