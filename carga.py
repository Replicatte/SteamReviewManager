import pickle

print("Introduce el nombre del pickle a cargar:")

b = pickle.load(open('data/summary_ATLAS_ES.pickle', 'rb'))

print(b)
#for key,value in b.items():
    #value['review']
    #break
