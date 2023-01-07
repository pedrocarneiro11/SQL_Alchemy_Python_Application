import pymongo as pyM

client = pyM.MongoClient("mongodb+srv://pedro123:<password>@cluster2mongodbatlas.hcqqrn7.mongodb.net/test")

db = client.test
collection = db.test__collection
print(db.test__collection)