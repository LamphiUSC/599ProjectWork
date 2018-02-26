import csv
import json

sci_fi_database_reader = open('sci-fi_database.csv', 'r')
sci_fi = csv.reader(sci_fi_database_reader)

with open('ufo_awesome.json') as json_data:
    ufo_data = json.load(json_data)

sci_fi_output = open('sci_fi_output.csv','w')

sci_fi_dict = {}
for row in sci_fi:
	year=row[0]
	if year.isdigit():
		if year in sci_fi_dict:
			sci_fi_dict[year]=sci_fi_dict[year]+1
		else:
			sci_fi_dict[year]=1

ufo_dict = {}
for row in ufo_data:
	year = row['sighted_at'][0:4]
	if year ==0:
		year = int(row['reported_at'][0:4])
	if year in ufo_dict:
		ufo_dict[year] = ufo_dict[year]+1
	else:
		ufo_dict[year]= 1
yes_counter=0
no_counter=0
sci_fi_output.write("year,Number of sci_fi movies released,Number of ufo sightings, Possibility of ufo_sighting being a dillusion after a sci-fi movie being released?\n")
for year in sci_fi_dict:
	if year in ufo_dict:
		if(ufo_dict[year]/sci_fi_dict[year]<2):
			possible = "Yes"
			yes_counter = yes_counter+1
		else:
			possible = "No"
			no_counter = no_counter+1
		sci_fi_output.write(str(year)+','+str(sci_fi_dict[year])+','+str(ufo_dict[year])+','+possible+'\n')

print "Number of possible true dillusions "+str(yes_counter)
print "Number of possible false dillusions "+str(no_counter)
total_counter = yes_counter+no_counter
percent_of_yes = float(yes_counter)/total_counter*100
percent_of_no = float(no_counter)/total_counter*100
print "Percent of possible true dillusions "+str(percent_of_yes)
print "Percent of possible false dillusions "+str(percent_of_no)


