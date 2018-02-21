import pickle

pdata_900_30k = []
for i in range(0,20):
    fname = "ufo_region_data"+str(i)+".pickle"
    with open(fname, 'rb') as f1:
        data = pickle.load(f1)
        #print(len(data))
        pdata_900_30k = pdata_900_30k + data
print(len(pdata_900_30k))
with open("pdata_0_10k.pickle", 'wb') as f2:
    pickle.dump(pdata_900_30k, f2)