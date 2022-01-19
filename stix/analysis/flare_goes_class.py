#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Flare processing
   what are done in this script:
   - attach ephemeris to each flare
   - determine goes class
   - store results in the flare list database
"""
import numpy as np
from stix.core import mongo_db as db
from stix.spice import stix_datetime
from stix.core import config
from stix.spice import solo
threshold=0

mdb = db.MongoDB()

flare_db=mdb.get_collection('flares')

def get_first_element(obj):
    if not isinstance(obj, dict):
        return obj
    new_obj = {}
    for key,val in obj.items():
        if isinstance(val, list):
            new_obj[key]=val[0]
        else:
            new_obj[key]=val
    return new_obj
def goes_flux_to_class(x):
    x=float(f'{x:.1e}')
    if x==0:
        return 'NA'
    elif x<1e-7:
        return 'A'
    elif x<1e-6:
        return f'B{x/1e-7:.1f}'
    elif x<1e-5:
        return f'C{x/1e-6:.1f}'
    elif x<1e-4:
        return f'M{x/1e-5:.1f}'
    else:
        return f'X{x/1e-4:.1f}'
def get_goes_info(start, end):
    data = mdb.get_goes_fluxes(start, end)
    last_time=0
    start_times=[]
    low_name='0.1-0.8nm'
    high_name='0.05-0.4nm'
    peak_time_low=0
    peak_flux_low=0
    peak_flux_high=0
    peak_time_high=0
    for d in data:
        unix = d['unix_time']
        flux=d['flux']
        if d['energy']==low_name and flux>peak_flux_low:
            peak_flux_low=flux
            peak_time_low=unix

        if d['energy']==high_name and flux>peak_flux_high:
            peak_flux_high=flux
            peak_time_high=unix


    goes_class=goes_flux_to_class(peak_flux_low)
    return  (peak_time_low, peak_flux_low, peak_time_high, peak_flux_high, goes_class)
def find_goes_class_flares_in_file(file_id):
    print(f'processing flares in file {file_id}')
    fdb=mdb.get_collection('flares')
    flares=flare_db.find({'run_id':file_id, 'hidden':False})
    if not flares:
        print(f'Flare not found in  {file_id} !')
        return
    goes_class_list=[]
    for doc in flares:
        peak_utc, goes_class,goes_estimated=get_flare_goes_class(doc)
        goes_class_list.append((peak_utc, goes_class, goes_estimated))

    return goes_class_list
def estimate_goes_class(counts, dsun):
    #details see https://pub023.cs.technik.fhnw.ch/wiki/index.php?title=GOES_Flux_vs_STIX_counts
    #https://docs.google.com/spreadsheets/d/19dRkncYAFjbsJUrkOYOhfX_oxGNIkQMvRfS15UkYRDM/edit?usp=sharing
    pars=[-6.576,0.2675, -0.1273,0.02618]
    mean_error=0.5
    #result={'min':None,'max':None, 'center':None}
    try:
        x =np.log10(counts/dsun)
    except ZeroDivisionError:
        x=0

    f=lambda x: goes_flux_to_class(10 ** (pars[0]+pars[1]*x+pars[2]*x**2+pars[3]*x**3))
    return {'min': f(x -mean_error),  'center': f(x),  'max':f(x+mean_error)}



def get_flare_goes_class(doc):
    start_unix=doc['start_unix']
    end_unix=doc['end_unix']
    start_utc=stix_datetime.unix2utc(start_unix)
    end_utc=stix_datetime.unix2utc(end_unix)
    peak_utc=doc['peak_utc']

    
    try:
        peak_counts=doc['LC_statistics']['lc0']['signal_max']
    except KeyError:
        print('peak counts not found')
        peak_counts=doc['peak_counts']

    if peak_counts<=threshold:
        print(f"Ignored flares {doc['_id']}, peak counts < {threshold}")
        return


    ephs=solo.get_solo_ephemeris(peak_utc, peak_utc)
    eph=get_first_element(ephs)
    dsun=eph.get('sun_solo_r',1)
    try:
        delta_lt=eph['light_time_diff']
    except (KeyError, IndexError):
        delta_lt=0
    
    peak_time_low, peak_flux_low, peak_time_high, peak_flux_high, goes_class=get_goes_info(start_unix+delta_lt, end_unix+delta_lt)
    bkg_subtracted_counts=peak_counts-doc['baseline']

    estimated_class=estimate_goes_class(bkg_subtracted_counts, dsun)
    #print(estimated_class)

    flare_db.update_one(
            {'_id':doc['_id']},
            {'$set':{
                'goes':{
                    'low':{'unix_time':peak_time_low, 'utc': stix_datetime.unix2utc(peak_time_low), 'flux':peak_flux_low},
                    'high':{'unix_time':peak_time_high, 'utc': stix_datetime.unix2utc(peak_time_high), 'flux':peak_flux_high},
                    'class':goes_class,
                    'estimated_class':estimated_class,
                    },
                'ephemeris':eph
                }
            })
    return stix_datetime.unix2utc(peak_time_low), goes_class, estimated_class
            

if __name__ == '__main__':
    import sys
    file_ids=[]
    if len(sys.argv) < 2:
        print('flare_processing file_number')
    elif len(sys.argv) == 2:
        file_ids.append(int(sys.argv[1]))
    else:
        file_ids=[x for x in range(int(sys.argv[1]),
                       int(sys.argv[2])+1)]
    for _id in file_ids:
        find_goes_class_flares_in_file(_id)


