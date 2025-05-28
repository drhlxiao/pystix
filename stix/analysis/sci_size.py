#this is script is to fixed the issue of Level 1 data, which have multiple pixel mask values in the same packets
# hualin.xiao created on May. 24, 2022

import sys
import os
import json
from pprint import pprint
from stix.core import mongo_db as db

mdb = db.MongoDB()
col_bsd = mdb.get_collection("bsd")
col_pkts = mdb.get_collection("packets")

def get_size(pkt_ids):
    total_size = 0 
    hashes = []  # Corrected variable name
    pkt_headers = col_pkts.find({'_id': {'$in': pkt_ids}}, {'header': 1, 'hash': 1})
    for pkt in pkt_headers:
        header = pkt['header']


        h = pkt.get('hash', '')
        if h in hashes:  # Use correct variable name and simplify condition
            continue
        
        total_size += header['raw_length']
        hashes.append(h)  # Add hash to hashes list to track seen hashes
    
    return total_size

def fill_all():
    bsd_docs = col_bsd.find().sort('_id',-1).limit(1000)
    for doc in bsd_docs:
        pkt_ids = doc.get("packet_ids", [])
        total_size = get_size(pkt_ids)
        bsd_id = doc['_id']
        
        print(f"Updating BSD document {bsd_id} with total size {total_size}")
        
        # Update the document in MongoDB
        col_bsd.update_one({'_id': bsd_id}, {'$set': {'total_size': total_size}})



def process_file(file_id):
    bsd_docs = col_bsd.find({'run_id':file_id})
    for doc in bsd_docs:
        pkt_ids = doc.get("packet_ids", [])
        total_size = get_size(pkt_ids)
        bsd_id = doc['_id']
        print(f"Updating BSD document {bsd_id} with total size {total_size}")
        # Update the document in MongoDB
        col_bsd.update_one({'_id': bsd_id}, {'$set': {'total_size': total_size}})


