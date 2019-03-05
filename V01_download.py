import requests
import json
import time
import pickle
#Personal
import gameIDs

def main():
    start_time = time.time()
    used = []
    reviewDict = {}

    #-- PARAMETERS --
    isJSON = 'json=1'
    language = 'language=english'
    rFilter = 'filter=updated'
    #Aplicar para limitar dias
    dayRange = 'day_range=30'
    reviewType = 'review_type=all'
    purchaseType = 'purchase_type=all'
    
    startOffset = 'start_offset=0'
    numPerPage = 'num_per_page=0'

    gamecode =  gameIDs.PORTAL2


    reqString = 'http://store.steampowered.com/appreviews/'+ gamecode +'?'+isJSON+'&'+language+'&'+rFilter+'&'+startOffset+'&'+reviewType+'&'+purchaseType+'&'+numPerPage  
    req = requests.get(reqString)

    print()
    checkStatusCode(req)

    json_data  = json.loads(req.text)
    summary = json_data['query_summary']
    print("NÚMERO TOTAL DE RESEÑAS:")
    print(summary['total_reviews'])
    totalReviews = summary['total_reviews']
    BATCH_SIZE = 100

    #for index in range(0,summary['total_reviews'],BATCH_SIZE):
    for index in range(0,totalReviews,BATCH_SIZE):

        startOffset = 'start_offset=' + str(index)
        numPerPage = 'num_per_page=' + str(BATCH_SIZE)
        
        reqString = 'http://store.steampowered.com/appreviews/'+ gamecode +'?'+isJSON+'&'+language+'&'+rFilter+'&'+startOffset+'&'+reviewType+'&'+purchaseType+'&'+numPerPage  
        req = requests.get(reqString)
        print()
        checkStatusCode(req)
        #print(req.headers)
        #print(req.json())
        json_data  = json.loads(req.text)
        reviews = json_data['reviews']
        

        
        print("Index "+ str(index)+"/"+ totalReviews +" ~ numDescargas " + str(len(reviews))+" ~ numDescargas " + str(len(reviews)))
        print()
        print('#########################################################################')
        #Para cada reseña
        for revIndex in range(len(reviews)):
            revID = reviews[revIndex]['recommendationid']
            #print(revID)
            if revID in used:
                #FIXME: Quitar el input 
                print('ALREADY USED IN DICT ->' + str(revID) + ' @index ' + str(used.index(revID)))
               
            else:
                used.append(revID)
                reviews[revIndex].pop('recommendationid')
                reviewDict[revID] = reviews[revIndex]

        if len(reviews) != BATCH_SIZE: 
            print("Fin por tamaño? " + str(len(reviewDict))+'/'+totalReviews )
            
        
        #print('#########################################################################')
   
    # BEWARE DATAFILES
    summary_filename = 'data/summary_PORTAL2_EN.pickle'
    data_filename = 'data/data_PORTAL2_EN.pickle'

    print("     PRECAUCIÓN!")
    print(" Estas a punto de substituir " + data_filename + "y su sumario.")
    input()
    with open(summary_filename, 'wb') as handle:
        pickle.dump(summary, handle, protocol=pickle.HIGHEST_PROTOCOL)

    with open(data_filename, 'wb') as handle:
        pickle.dump(reviewDict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print("---TIEMPO TOTAL %s s ---" % (time.time() - start_time))
    return 

















def makeReviewRequest(language,filter,startOff,reviewType,purchaseType,numPerPage):
    #TODO checkParameters
    return 

def checkStatusCode(r):

    if r.status_code == requests.codes.ok:
        print("STATUS CODE OK")
    else:
        print("WRONG STATUS CODE: ")
        print(r.status_code)
    return 


    
if __name__ == "__main__": main()
    