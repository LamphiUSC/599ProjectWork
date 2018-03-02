import pickle

with open('ufo_airport_scifi_census_merged.tsv', 'r') as tsvFile:
    lines = tsvFile.readlines()


count = 0
listOfCols = []
dataDict = {}

for line in lines:
    if line == '\n':
        continue
    data = line.replace('\n', '').split("\t")
    if count == 0:
        listOfCols = data
        # print(listOfCols)
    else:
        index = 0
        isEmpty = False
        for word in data:
            word = word.replace('\n', '')

            if listOfCols[index] in dataDict:
                colname = listOfCols[index]
                valueList = dataDict[listOfCols[index]]
                valueList.append(word)
                dataDict[listOfCols[index]] = valueList
                if listOfCols[index] == "County" and word == '':
                    valueList = dataDict["Population Density"]
                    valueList.append("")
                    dataDict["Population Density"] = valueList
                    valueList = dataDict["Housing Denisty"]
                    valueList.append("")
                    dataDict["Housing Denisty"] = valueList
                    valueList = dataDict["Rural?"]
                    valueList.append("")
                    dataDict["Rural?"] = valueList
            else:
                valueList = [word]
                dataDict[listOfCols[index]] = valueList
            index = index + 1

    count = count + 1

print( len(dataDict["Housing Denisty"]))

print(dataDict["Housing Denisty"])

# pickle.dump( dataDict, open( "featureDict.p", "wb" ) )
pickle.dump( dataDict, open( "featureDictVer2.p", "wb" ), protocol=2 )