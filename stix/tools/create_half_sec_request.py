# author: Hualin Xiao
# pre-process science data, merge bulk science data packets and write merged data to json files
# so that web client side could load the data quickly
import sys
import os
import json
import numpy as np
from datetime import datetime
from stix.core import datatypes as sdt
from stix.spice import datetime
from stix.core import mongo_db as db
from stix.core import logger
from stix.core import config
mdb = db.MongoDB()

def create_req(_id, start_unix, duration ):
    start_utc = sdt.unix2utc(start_unix)
    end_unix=start_unix+duration
    end_utc = sdt.unix2utc(end_unix)
    form={
    "_id" : _id,
    "email" : "bot@stix",
    "flare_id" : "-1",
    "data_volume" : "0",
    "data_volume_upper_limit" : "0",
    "username" : "",
    "execution_date" : "",
    "author" : "bot",
    "subject" : "IOR 374: 40s top only",
    "purpose" : "Solar Flare",
    "request_type" : "L1",
    "start_utc" :start_utc, 
    "duration" : str(duration),
    "time_bin" : "40",
    "detector_mask" : "0xFFF8E2FF",
    "pixel_mask" : "0xF",
    "emin" : "1",
    "emax" : "17",
    "eunit" : "1",
    "scaling_factor" : "0",
    "priority" : "1",
    "description" : "",
    "volume" : -1,
    "start_unix" : start_unix,
    "end_unix" : end_unix,
    "end_utc" : end_utc,
    "creation_time" : datetime.now()
    "status" : 0,
    "hidden" : False,
    "reviewers" : "Hualin Xiao",
    }
    
def run():
    start_id=66552
    for 
    db= mdb.get_collection('data_requests')
    db.insert_one(form)
