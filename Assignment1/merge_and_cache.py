import pickle
import json

from pymongo import MongoClient

db = MongoClient().ufo.cities


with open('ufo_awesome.json') as json_data:
    ufo_data = json.load(json_data)

# with open("pdata2.pickle", 'rb') as f1:
with open("pdata_0_10k.pickle", 'rb') as f1:
        data = pickle.load(f1)

empty_dict_file = open("empty_dict_file1.txt",'w')

count=0
ctr=0
# for i,value in enumerate(ufo_data):
for i,value in enumerate(data):
    try:
    	if not db.find_one({"location": value['location']}):
	    	if data[i]:
	    		latitude=data[i]['lat']
	    		longitude=data[i]['lon']
	    		country=data[i]['country']
	    		
	    		# location=data[i]['location']
	    		location = value['location']
	    		try:
	    			state=data[i]['state']
	    		except:
	    			if country is not "US":
	    				state=""
	    			else:
	    				# print(str(i)+"\t\t"+str(data[i])+"\t\t"+str(ufo_data[i])+"\n\n\n")
	    				print(str(i)+"\t\t"+str(data[i])+"\n\n\n")
	    		region=data[i]['region']
	    		db.insert_one({"location": location, "latitude": latitude, "longitude": longitude,"state": state, "country": country, "region": region})
	    	else:
	    		# empty_dict_file.write(str(ufo_data[i])+"\n")
	    		empty_dict_file.write(str(location)+"\n")

	    		ctr=ctr+1
    except Exception as e: 
    	count=count+1
    	print(e)
    	# print(str(i)+"\t\t"+str(data[i])+"\t\t"+str(ufo_data[i])+"\n\n\n")
    	print(str(i)+"\t\t"+str(data[i])+"\n\n\n")

print("Errors = " + str(count)+" ,empty dicts = "+str(ctr))