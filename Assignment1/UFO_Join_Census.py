import json
import csv
from collections import defaultdict


stateInitials = {'AL':'Alabama','AK':'Alaska','AZ':'Arizona','AR':'Arkansas','CA':'California','CO':'Colorado',
'CT':'Connecticut','DE':'Delaware','FL':'Florida','GA':'Georgia','HI':'Hawaii','ID':'Idaho','IL':'Illinois','IN':'Indiana',
'IA':'Iowa','KS':'Kansas','KY':'Kentucky','LA':'Louisiana','ME':'Maine','MD':'Maryland','MA':'Massachusetts','MI':'Michigan',
'MN':'Minnesota','MS':'Mississippi','MO':'Missouri','MT':'Montana','NE':'Nebraska','NV':'Nevada','NH':'New Hampshire',
'NJ':'New Jersey','NM':'New Mexico','NY':'New York','NC':'North Carolina','ND':'North Dakota','OH':'Ohio','OK':'Oklahoma',
'OR':'Oregon','PA':'Pennsylvania','RI':'Rhode Island','SC':'South Carolina','SD':'South Dakota',
'TN':'Tennessee','TX':'Texas','UT':'Utah','VT':'Vermont','VA':'Virginia','WA':'Washington','WV':'West Virginia',
'WI':'Wisconsin','WY':'Wyoming'}




UFOStateYear ={} # dictionary with tuple (state, year) as key and value is count of sightings
CensusStateYear = {} # dictionary with tuple (state, year) as key and value is tuple of (population density, housing density)
joinedResultDict = defaultdict(list)

with open('2000Census.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    print(type(reader))
    next(reader, None)
    next(reader,None)
    for row in reader:
        state = row['GCT_STUB.display-label'].strip()
        if state in stateInitials.values():
            val = (float(row['HC08'].strip()),float(row['HC09'].strip()))
            state  = row['GCT_STUB.display-label'].strip()
            for y in range(1991, 2001):  # years from 1991 to 2000
                CensusStateYear[(state, y)] = val
        else:
            continue

with open('2010Census.csv') as csvfile:
    reader = csv.DictReader(csvfile)
    print(type(reader))
    next(reader, None)
    next(reader,None)
    for row in reader:
        state = row['GCT_STUB.display-label'].strip()
        if state in stateInitials.values():
            try:
                val = (float(row['SUBHD0401'].strip()),float(row['SUBHD0402'].strip()))
            except:
                print(row)
            state  = row['GCT_STUB.display-label'].strip()
            for y in range(2001, 2011):  # years from 1991 to 2000
                CensusStateYear[(state, y)] = val
        else:
            continue
print(CensusStateYear)

#print(len(CensusStateYear.keys()))


with open('ufo_awesome.json',encoding = "utf-8") as json_data:
    ufo_data = json.load(json_data)

# r = ufo_data[0]
# year = int(r['sighted_at'][0:4])
# if year ==0:
#     year = int(r['reported_at'][0:4])
# state = stateInitials[r['location'].split(",")[1].strip()]
# print(state)
# t = (state, year)
# print(type(t))

for r in ufo_data:
    year = int(r['sighted_at'][0:4])
    if year ==0:
        year = int(r['reported_at'][0:4])
    stateInitial = r['location'].split(",")[1].strip()
    if(stateInitial not in stateInitials.keys()): # invalid state e.g: location CANADA, BC
        continue
    else:
        state = stateInitials[stateInitial]
        t = (state, year)
        if t in UFOStateYear:
            UFOStateYear[t] = UFOStateYear[t]+1
        else:
            UFOStateYear[t] = 1

censusSet = set(CensusStateYear)
UFOStateSet = set(UFOStateYear)

for key in censusSet.intersection(UFOStateSet):
    joinedResultDict[key].append(UFOStateYear[key])
    temp = CensusStateYear[key] # () tuple population density, housing density
    joinedResultDict[key].append(temp[0])
    joinedResultDict[key].append(temp[1])




resultOutputFile = open("CensusOutput.csv",'w')
resultOutputFile.write('State'+','+'Year'+','+'SightingCount'+','+'Population Density'+','+'Housing Density'+'\n')
for k, v in joinedResultDict.items():
    try:
        resultOutputFile.write(str(k[0])+','+str(k[1])+','+str(v[0])+','+str(v[1])+','+str(v[2])+'\n')
    except:
        print(k,joinedResultDict[k])




#print(joinedResultDict)  # <(StateName, Year), [UFOSightingsCount, population density, housing density]>

#print(sum(UFOStateYear.values()))  ## 51547 sightings for valid 50 US states


        # change key of the dict from initial of state to state name e:g IA to IOWA
#dict((d1[key], value) for (key, value) in d.items())