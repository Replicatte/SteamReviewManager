import requests
import json
import time
import logging
from pymongo import MongoClient
client = MongoClient()
BATCH_SIZE = 100
myDb = client["SteamReviewDB"]
myGameCol = myDb["Games"]
myReviewCol = myDb["Reviews"]
mySummaryCol = myDb["Summaries"]



def downloadSummaryOfGame(appid,language):
    #-- PARAMETERS --
    isJSON = 'json=1'
    idiom = 'language='+language
    rFilter = 'filter=updated'
    #Aplicar para limitar dias
    #dayRange = 'day_range=?'
    reviewType = 'review_type=all'
    purchaseType = 'purchase_type=all'
    
    startOffset = 'start_offset=0'
    numPerPage = 'num_per_page=0'

    #Get New summary
    reqString = 'http://store.steampowered.com/appreviews/'+ str(appid) +'?'+isJSON+'&'+idiom+'&'+rFilter+'&'+startOffset+'&'+reviewType+'&'+purchaseType+'&'+numPerPage  
    req = requests.get(reqString)
    json_data  = json.loads(req.text)
    newSummary = json_data['query_summary']

    newSummary['lastUpdateStartUTC'] = time.gmtime()
    
    return mySummaryCol.insert_one(newSummary).inserted_id

def setSummaryEndTime(summId):
    mySummaryCol.update_one({'_id': summId},{"$set":{"lastUpdateEndUTC": time.gmtime()}},upsert=False)


'''
game - Game to download the reviews from
language - What language do we want for the reviews
'''
def downloadGameReviews(game,language):
   
    appid = game['appid']

    summaryId = downloadSummaryOfGame(appid,language)

    used = []
    ourSummary = mySummaryCol.find_one({'_id':summaryId})
    totalReviews = ourSummary['total_reviews']
    #Can be multiple downloads / summaries of a game?


    #-- PARAMETERS --
    isJSON = 'json=1'
    idiom = 'language='+language
    rFilter = 'filter=updated'
    #Aplicar para limitar dias
    #dayRange = 'day_range=?'
    reviewType = 'review_type=all'
    purchaseType = 'purchase_type=all'
    
    startOffset = 'start_offset=0'
    numPerPage = 'num_per_page=0'
    
    #Start Downloading Reviews
    for index in range(0,totalReviews,BATCH_SIZE):
        startOffset = 'start_offset=' + str(index)
        numPerPage = 'num_per_page=' + str(BATCH_SIZE)
        
        reqString = 'http://store.steampowered.com/appreviews/'+ str(appid) +'?'+isJSON+'&'+language+'&'+rFilter+'&'+startOffset+'&'+reviewType+'&'+purchaseType+'&'+numPerPage  
        req = requests.get(reqString)

        #checkStatusCode(req)
        json_data  = json.loads(req.text)
        reviews = json_data['reviews']
        repetidos = 0
        print("\r"+game['name']+"("+language+")" + ":  Index "+ str(index)+"/"+ str(totalReviews) +" ~ numDescargas " + str(len(reviews))+" ~ " + str(index/totalReviews * 100)  + '%', end='')
        
        #Para cada reseña
        for revIndex in range(len(reviews)):
            revID = reviews[revIndex]['recommendationid']
            if revID in used:
                #FIXME: Quitar el input
                print()
                print('ALREADY USED IN DICT -> ' + str(revID) + ' @index ' + str(used.index(revID)))
                repetidos+=1
            else:
                used.append(revID)
                reviews[revIndex]['summaryID'] = summaryId
                reviews[revIndex]['gameID'] = appid
                #The game is now updated
                myReviewCol.insert_one(reviews[revIndex])
                #print(json.dumps(reviews, indent=4, sort_keys=True))
                #input()
        if len(reviews) != BATCH_SIZE:
            print()

    print('--  Repeated '+ str(repetidos) + '  --')
    #input()
    setSummaryEndTime(summaryId)

    return





def loggerConfig():
    # Create a custom logger
    logger = logging.getLogger(__name__)

    # Create handlers
    c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler('file.log')
    c_handler.setLevel(logging.WARNING)
    f_handler.setLevel(logging.ERROR)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)




def main():
    loggerConfig()
    start_time = time.time()
    index = 0
    #TODO not in spanish
    for game in myGameCol.find({'languages':{'$regex': 'Spanish'}}):
        index+=1
        print('Game Nº ' + str(index))
        if index > 14:
            downloadGameReviews(game,'spanish')

    '''    
    empty = {}
    for game in myCol.find():
        appid = game['appid']
        myCol.update_one({'appid': appid},{"$set":{"reviews": empty}},upsert=False)
        print("ok")
    '''
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
    