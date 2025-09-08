import csv
import pymongo
connect = pymongo.MongoClient()
db = connect["stix"]
bsd= db['bsd']
images = db['flare_images']
flare = db['flares']
bsd.update_many({},{'$unset':{'image_ids':''}})
flares.update_many({},{'$unset':{'image_ids':'','flare_image_ids':''}})
images.delete_many({})


