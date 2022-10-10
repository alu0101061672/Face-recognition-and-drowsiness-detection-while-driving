from pymongo import MongoClient

client = MongoClient("mongodb+srv://alu0100889635:ZeP2jDqVfrYJnFiL@facialrecognitiondb.3gpysl0.mongodb.net/?retryWrites=true&w=majority")
db = client.facialRecognitionDB
drivers_collection = db.get_collection("drivers")
licenses_collection = db.get_collection("licenses")
vehicles_collection = db.get_collection("vehicles")