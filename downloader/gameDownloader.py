import requests
import json
import time
import pickle
import logging
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



def getGames():
    reqString = 'http://steamspy.com/api.php?request=all'  
    #reqString = 'http://api.steampowered.com/ISteamApps/GetAppList/v2'  
    req = requests.get(reqString)
    return json.loads(req.text)


def getDetailsOfGame(appid):
    reqString = 'http://steamspy.com/api.php?request=appdetails&appid=' + str(appid)
    detailReq = requests.get(reqString)
    return json.loads(detailReq.text)



def main():
    #Time tracker
    start_time = time.time()

    loggerConfig()
    #Conect to the mongoDB 
    from pymongo import MongoClient
    client = MongoClient()

    myDb = client["SteamReviewDB"]
    myCol = myDb["Games"]

    globalUTC = time.gmtime()
    print(time.strftime("%a, %d %b %Y %H:%M:%S +0000", globalUTC))
    #Makes a request petition for getting all the posible games
    games = getGames()
    #games = getGames()['applist']['apps']

    logging.info('Starting Download: ' + str(len(games)) + ' games')
    
    '''
    Key -> Appid
        Values:
        appid
        name
        developer
        publisher
        score_rank
        positive
        negative
        userscore
        owners
        average_forever
    '''
    #We have to add all of them to the database?
    gamenum = 0
    progres = 0
    for key,value in games.items():
        numOfReviews = value['positive'] + value['negative']
        #Only get data of the games with reviews.
        if(numOfReviews > 0):
            print("Processing appid: " + str(key) + " AKA ["+ value['name'] +"] "+ str(progres / len(games) *100) + "%")
            
           
            '''
            print(json.dumps(details, indent=4, sort_keys=True))
            input() [This War of Mine]
            '''
            details = getDetailsOfGame(key)
            details['lastUpdateUTC'] = globalUTC
            

            foundDoc = myCol.find_one({'appid': str(key)})
            #Is already in the collection?
            if foundDoc == None:
                details['reviews'] = []
                try:

                    myCol.insert_one(details)
                except:
                    print("An exception occurred while inserting . . .")
                    logging.warning("COULDN\'T INSERT " + str(key) + " AKA ["+ value['name'] +"] " )
                
            else:
                #TODO have to get the reviews to save them before updating
                try:

                    details['reviews'] = foundDoc['reviews']

                    myCol.update_one({'appid': str(key)},details)

                except:
                    print("An exception occurred while updating . . .")
                    logging.warning("COULDN\'T UPDATE " + str(key) + " AKA ["+ value['name'] +"] " )

               
            gamenum+=1
        else:
            print("NOT Processing appid: " + str(key) + " AKA ["+ value['name'] +"]")
            print("No reviews. No need of storage. (" + str(numOfReviews) + ")")
        print("--------------------------------------------------------------")
        progres+=1


    logging.info('END Downloaded/Updated ' + str(gamenum)+ "/" + str(len(games)) + ' games')
    print("TOTAL EVALUATED:")
    print(str(gamenum)+ "/" + str(len(games)))
    print("---TIEMPO TOTAL %s s ---" % (time.time() - start_time))
    #for i in range(len(gamelist)):
        #print(gamelist[i][])

if __name__ == "__main__": main()
    
