from pymongo import MongoClient
import pprint
import timeit
client = MongoClient()
db = client['stix']
packets_col = db['packets']
runs_col = db['raw_files']
timeit.timeit(packet_col.find({}, {"header_id": 100000}), number=1000)