import requests
import json
import time
import pickle

def main():
    start_time = time.time()
    reqString = 'http://steamspy.com/api.php?request=all'  
    req = requests.get(reqString)
    games = json.loads(req.text)
    #for key,value in games.items():
    gamelist = []
    for key,value in games.items():
        gamelist.append(value)

    for i in range(20):
        print(gamelist[i])


if __name__ == "__main__": main()
    