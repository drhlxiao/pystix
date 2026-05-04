#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Compute integration times
    Steps:
    1) Find the rotation buffer integration times
    2) estimate integration time  

"""

import os
import sys
sys.path.append('.')
from scipy import signal
import math
import numpy as np
from stix.utils import bson
from matplotlib import pyplot as plt
from stix.core import mongo_db as db
from stix.spice import time_utils
from stix.core import logger
from stix.spice import solo
from stix.analysis import ql_analyzer as qla
from datetime import datetime

logger = logger.get_logger()

mdb = db.MongoDB()

default_rot_tmin=0.5
default_rot_tmax=20
default_rot_threshold=1800
#rotation buffer configuration


#def get_rotating_buffer_config(max_time, min_time=None):
def get_rotating_buffer_config(end_unix_time, start_unix_time=None):

    rot_config={312: [], 313: [], 314:[]}
    config_db= mdb.get_collection('config')

    if not start_unix_time:
        start_unix_time= end_unix_time



    for _id in rot_config.keys():
        # First Query, find the last config cmd
        query1 = {
            'type': 'asw',
            'parameter': _id,
            'execution_unix': { '$lte': start_unix_time}
        }
        print(query1)

        result1 = config_db.find(query1).sort('execution_unix', -1).limit(1)

        # Second Query
        #find if any such command executed within the time range of the file
        query2 = {
            'type': 'asw',
            'parameter': _id,
            'execution_unix': { '$gte': start_unix_time, '$lte': end_unix_time}
        }
        print(query2)

        result2 = config_db.find(query2)

        # Combine Results
        rows= list(result1) + list(result2)
        for row in rows:
            #print(row)
            
            rot_config[_id].append( {'time': row['execution_unix'], 'value': row['value']})
    return rot_config

def get_rot_config(configs, unix_time):
    tmin=default_rot_tmin
    tmax=default_rot_tmax
    thr=default_rot_threshold
    

    for row in configs[312]:
        if unix_time > row['time']:
            tmin=0.1*(int(row['value'])+1)
    for row in configs[313]:
        if unix_time > row['time']:
            tmax=0.1*(int(row['value'])+1)
    for row in configs[314]:
        if unix_time > row['time']:
            thr=row['value']

    return tmin, tmax, thr


def process_file(file_id):
    print("Processing file:", file_id)
    packets = mdb.select_packets_by_run(file_id, SPIDs=54118)
    if not packets:
        #print("No QL packet found in the file:{file_id}")
        return
    print("Parsing light curves...")
    data = qla.LightCurveAnalyzer.parse(packets)
    if data is None:
        return
    unix_time = data['time']  # set to the center of a bin
    configs = get_rotating_buffer_config(unix_time[-1], unix_time[0])
    #print(data['lcs'])
    #print("Config:")
    #print(configs)
    #print("start, end:", time_utils.unix2utc(unix_time[-1]), time_utils.unix2utc(unix_time[0] ))
    #print(data['lcs'])
    lightcurve =np.sum([v for k,v in data['lcs'].items() if int(k) in (0,1)] ,axis=0)
    #sum counts of all energy bands
    triggers=data['triggers']

    res = {'t': [], 'tbin': [], 'counts': [],  'num_tbins': [], 'time_bin_trig_sum':[],'config':configs}
    s = 0
    last_time = 0

    trig_sum=0
    #used to store summed triggers of the time bin print(triggers)
    

    for t, c, tr in zip(unix_time, lightcurve,triggers ):
        t = int(t)
        c = int(c)
        trig_sum=tr
        if last_time == 0:
            last_time = t
            continue

        min_tbin, max_tbin, thr=get_rot_config(configs, t)
        print("Final settings:", min_tbin,max_tbin,thr)

        

        if s > 0 and (s >= thr or t - last_time >= max_tbin
                or c >= thr):  # close the opening time bin anyway
            # close last time bin
            tbin = round(min([max_tbin, t - last_time]), 1)
            #print("====================reset timebin====")
            #print(f'case1: current_accumulated: {s}, {thr=}, current_tbin_count: {c},{tbin=}')
            res['tbin'].append(tbin)
            res['num_tbins'].append(1)
            res['t'].append([last_time, t])
            res['counts'].append(s)
            res['time_bin_trig_sum'].append(trig_sum)
            trig_sum=0
            # print(last_time, t,t-last_time,  c, tbin, s)
            s = 0
            last_time = t

        if c < thr:
            #print(f'-> {c}, {s}, {trig_sum}')

            s += c
            trig_sum+=tr
        else:
            #estimated sub-time bins
            #num_tbins = math.ceil(c / thr)
            #max_bins = math.ceil(4. / min_tbin)

            # replaced with the following code on 6 Nov. 2024, by Hualin Xiao
            # to fix the wrong estimated min bins issue when the onboard time-bins = 3 
            num_tbins = round(c / thr, 2)
            max_bins = round(4. / min_tbin,2)

            num_tbins = max(num_tbins,1)
            num_tbins = min(max_bins, num_tbins) #can not greater than the maximum time bins
            tbin = round(4. / num_tbins, 1)  # time step 0.1s

            #print('case2, tbin:',tbin)
            res['tbin'].append(tbin)
            res['num_tbins'].append(num_tbins) #number of timebins in 4 sec
            res['t'].append([t - 4, t])  #start time and end time
            res['counts'].append(c / num_tbins)  #average counts
            res['time_bin_trig_sum'].append(trig_sum/num_tbins)
            trig_sum=0
            # print(last_time, t, t-last_time, c, tbin, c/num_tbins)
            s = 0
            last_time = t

    res['start_unix'] = res['t'][0][0]
    res['end_unix'] = res['t'][-1][1]
    res['start_utc'] = time_utils.unix2utc(res['t'][0][0])
    res['end_utc'] = time_utils.unix2utc(res['t'][-1][1])
    res['file_id'] = file_id
    res = bson.dict_to_json(res)
    mdb.insert_time_bins(res, delete_existing=True)



if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('estimate_integration_times file_id_start, file_id_end')
    elif sys.argv[1]=='timebin':
        current_unix = datetime.now().timestamp()
        rows = get_rotating_buffer_config(current_unix)
        print(rows)


    elif len(sys.argv) >= 2:
        start_id = int(sys.argv[1])
        end_id = start_id
        if len(sys.argv) == 3:
            end_id = int(sys.argv[2])
        for i in range(start_id, end_id + 1):
            process_file(i)
