# -*- coding: utf-8 -*-
"""
    Flare detection algorithm
    Procedure:
    1) smoothing the lowest energy bin lightcurve using a butterworth low-pass filter
    2) searching for local maxima in the smoothed lightcurve
    This routine is called after a raw telemetry is being processed

"""
import os
import sys
import math
import matplotlib
import numpy as np
from scipy import signal
from pprint import pprint
from datetime import datetime, timedelta
from scipy import interpolate

from stix.core import logger
from stix.analysis import ql_analyzer as qla
from stix.spice import time_utils as st
from stix.core import mongo_db as db
from stix.core import datatypes as sdt
from matplotlib import pyplot as plt

sys.path.append('.')

logger = logger.get_logger()

mdb = db.MongoDB()
debug = True

PEAK_MIN_NUM_POINTS = 7  # peak duration must be greater than 28 seconds, used to determine energy range upper limit,
niter = 900
# matplotlib.use('qtagg' if debug else 'agg')
try:
    import ROOT
    ROOT_EXISTS = True
except ImportError:
    ROOT_EXISTS = False

DEFAULT_FLARE_LC_DIR = '/data/flare_lc'


qlc_att_db = mdb.get_collection('qlc_att_in')

def is_att_inserted(start_unix, end_unix):
    # correct the 4-10 keV light curves if ATT is inserted
    # called by the flare detection

    doc = qlc_att_db.find_one({
        'start_unix': {
            '$lte': end_unix
        },
        'end_unix': {
            '$gte': start_unix
        }
    })
    return bool(doc)

def correct_att():
    fdb=mdb.get_collection('flares')
    for flare in fdb.find().sort('_id',1):
        start, end = flare['start_unix'], flare['end_unix']
        att = is_att_inserted(start, end)
        if att:
            print("ATT inserted: ", flare['_id'], st.unix2utc(start), st.unix2utc(end))
        fdb.update_one({'_id':flare['_id']}, {'$set':{'att_in': att}})

    

correct_att()
