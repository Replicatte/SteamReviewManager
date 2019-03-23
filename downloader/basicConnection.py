from pymongo import MongoClient
client = MongoClient()

myDb = client["SteamReviewDB"]
myCol = myDb["Games"]
