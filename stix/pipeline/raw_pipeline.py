#!/usr/bin/env python3
# -*- encoding: utf-8 -*-
# @title        : Level 1 processing pipeline 
# @description  : STIX packet parser pipeline. It detects new files in the specified folder,
#                 parses the packets and stores the decoded packets in the MongoDB
# @author       : Hualin Xiao
# @date         : Feb. 11, 2020
#

import os
import sys
import glob
import argparse
from datetime import datetime
from stix.core import config
from stix.spice import time_utils as sdt
from stix.core import mongo_db
from stix.core import logger
from stix.core import parser as stp
from stix.mailer import mailer
from stix.fits import fits_creator
from stix.analysis import calibration
from stix.analysis import background_estimation as bkg
from stix.analysis import flare_detection
from stix.analysis import sci_packets_analyzer
from stix.analysis import integration_time_estimator
from stix.analysis import flare_goes_class as fgc
from stix.analysis import goes_downloader as gdl
from stix.imaging import imaging_task_manager as itm
from stix.pipeline import task_manager 


from stix.analysis import monitor

from stix.spice import spice_manager as spm
#from stix.flare_pipeline import flare_L1_analyzer as fla



#S20_EXCLUDED = True

logger = logger.get_logger()


actions={'calibration':True,
        'fits_creation':True,
        'flare_detection':True,
        'time_bins_simulation':True,
        'bsd_report_merging':True,
        'bsd_l1_preprocessing':False,
        'imaging':True,
        'bkg_estimation':True
        }
        

HOST = config.HTTP_PREFIX
goes=gdl.GOES()
daemon_config = config.get_config('pipeline.daemon')
mongodb_config = config.get_config('pipeline.mongodb')

MDB = mongo_db.MongoDB(mongodb_config['host'], mongodb_config['port'],
                       mongodb_config['user'], mongodb_config['password'])



def get_now():
    return datetime.now().isoformat()


class _Notification(object):
    def __init__(self):
        self.messages=[]
    def push(self, msg):
        self.messages.append(msg)
    def send(self):
        groups =MDB.get_group_users('operations') 
        if not groups:
            logger.error('can not find emails for operations team ')
            return
        receivers= groups[0]['user_emails']
        title = 'STIX operational message'
        bt='\n'+'='*50+'\n'
        content=str(bt).join(self.messages)
        logger.info('sending message..')
        logger.info(content)
        mailer.send_email(receivers, title, content)
        self.messages=[]
        #empty list
    
    def scan_housekeeping(self,file_id):
        warnings=monitor.HKMonitor.scan(file_id)
        content='\n'+'='*50+'\n'
        content+='Housekeeping monitoring:\n'
        if not warnings:
            content+='\n'.join(warnings)
        else:
            content+='\nNo abnormality detected.'
        self.messages.append(content)



    def append_pipeline_message(self, raw_filename, service_5_headers, summary, num_flares, goes_class_list):
        file_id = summary['_id']
        start = sdt.unix2utc(summary['data_start_unix_time'])
        end = sdt.unix2utc(summary['data_stop_unix_time'])
        content = f'New file: {raw_filename}\nObservation time: {start} - {end} \nRaw packets: {HOST}/view/packet/file/{file_id}\n'
        SCI_PACKET_SPIDS = ['54114', '54115', '54116', '54117', '54143', '54125']
        try:
            if '54102' in summary['summary']['spid'] or '54101' in summary[
                    'summary']['spid']:
                content += f'\nHousekeeping data: {HOST}/view/plot/housekeeping/file/{file_id}\n'
            if '54118' in summary['summary']['spid']:
                content += f'\nLight curves: {HOST}/view/plot/lightcurves?run={file_id}\n'
            content += f'\nL1A FITS files: {HOST}/view/list/fits/file/{file_id}\n'
            if summary['calibration_run_ids']:
                content += f'\nCalibration runs: {HOST}/view/plot/calibration/file/{file_id}\n'
            if [x for x in summary['summary']['spid'] if x in SCI_PACKET_SPIDS]:
                content += f'\nScience data: {HOST}/view/list/bsd/file/{file_id}\n'
        except Exception as e:
            logger.error(e)
        if service_5_headers:
            content += '\nSTIX Service 5 packets:\n'
            for header in service_5_headers:
                content += '\tAt {}, TM({},{}) {}\n'.format(
                    header['UTC'], header['service_type'],
                    header['service_subtype'], header['descr'])
        else:
            content += 'No Service 5 packet found in the file.\n'

        if num_flares > 0:
            content += '''\n{} solar flare(s) identified in the file\n \n'''.format(
                num_flares)
        else:
            content += '\n No solar flare detected.\n'
        if goes_class_list:
            content+='Peak UTC *  GOES class\n'
            for fl in goes_class_list:
                try:
                    est_goes=f', {fl[2]["center"]} (estimated)'
                except (IndexError, KeyError):
                    est_goes=''

                content+=f'{fl[0]}  -  {fl[1]}{est_goes} \n'
        self.messages.append(content)

Notification=_Notification()


def clear_ngnix_cache():
    '''
        remove ngnix cache if ngnix cache folder is defined in the configuration file
    '''
    files = glob.glob(daemon_config['ngnix_cache'])
    logger.info('Removing nginx cache..')
    for fname in files:
        try:
            os.remove(fname)
        except OSError as e:
            logger.error(str(e))
    logger.info('Nginx cache removed')




def find_new_telemetry_files():
    """
        Find new telemetry files in the folder specified in config.py
        returns: dict
        dictionary with a list of new files or empty dict
    """
    filelist = {}
    logger.info('checking new files ...')
    for instrument, selectors in daemon_config['data_source'].items():
        for pattern in selectors:
            filenames = glob.glob(pattern)
            for filename in filenames:
                if os.path.getsize(filename) == 0:
                    continue
                file_id = MDB.get_file_id(filename)
                if file_id == -2:
                    if instrument not in filelist:
                        filelist[instrument] = []
                    filelist[instrument].append(filename)
    return filelist



def piepeline_parsing_and_basic_analysis(instrument, filename, notification_enabled, debugging):
    spm.spice.load_kernels()
    #always load the latest kernel files
    logger.info(f'Start processing file {filename}')
    base = os.path.basename(filename)
    name = os.path.splitext(base)[0]
    num_flares = 0
    log_path = daemon_config['log_path']
    log_filename = os.path.join(log_path, name + '.log')
    logger.set_logger(log_filename, level=3)
    if debugging:
        logger.enable_debugging()
    parser = stp.StixTCTMParser()
    parser.config_mongodb(mongodb_config['host'], mongodb_config['port'],
                              mongodb_config['user'],
                              mongodb_config['password'], '', filename,
                              instrument)
    logger.info('{}, processing {} ...'.format(get_now(), filename))
    #if S20_EXCLUDED:
    parser.exclude_S20()
    #parser.set_store_binary_enabled(False)
    parser.set_packet_buffer_enabled(False)
    service_5_headers = None
    goes_class_list=None

    try:
        parser.parse_file(filename)
        service_5_headers = parser.get_alerts()
    except Exception as e:
        logger.error(str(e))
        return  None
    summary = parser.done()
    if not summary:
        return None

    file_id = summary['_id']

    if actions['bkg_estimation']:
        logger.info('Extracting background information from non-flaring times ..')
        try:
            bkg.process_file(file_id)
        except Exception as e:
            logger.error(str(e))

    if actions['flare_detection']:
        logger.info('Detecting flares..')
        try:
            num_flares = flare_detection.find_flares_in_one_file(
                file_id, lc_output_dir=daemon_config['flare_lc_snapshot_path'])
            if num_flares>0:
                goes_class_list=fgc.find_goes_class_flares_in_file(file_id)

            summary['num_flares']=num_flares
        except Exception as e:
            logger.error(str(e))
    if actions['time_bins_simulation']:
        try:
            integration_time_estimator.process_file(file_id)
        except Exception as e:
            logger.error(str(e))

    try:
        Notification.scan_housekeeping(file_id)
    except Exception as e:
        logger.error(str(e))

    try:
        Notification.append_pipeline_message(base, service_5_headers, summary,
                                       num_flares, goes_class_list)
    except Exception as e:
        logger.error(str(e))
    if actions['calibration']:
        logger.info('Analyzing calibration data ...')
        try:
            calibration_run_ids = summary['calibration_run_ids']
            report_path = daemon_config['calibration_report_path']
            for run_id in calibration_run_ids:
                calibration.process_one_run(run_id,create_pdf=True, pdf_path=report_path)
        except Exception as e:
            logger.error(str(e))
    clear_ngnix_cache()
    return file_id


def pipeline_fits_creation_packets_merging_and_imaging(file_id):
    logger.info('Creating fits files...')
    try:
        fits_creator.create_fits(file_id, daemon_config['fits_path'])
    except Exception as e:
        logger.error(str(e))
    logger.info(
            'Merging bulk science data and preparing json files for data browsers...')
    try:
        sci_packets_analyzer.process_packets_in_file(file_id)
    except Exception as e:
        logger.error(str(e))
    logger.info('preparing imaging inputs...')
    try:
        itm.register_imaging_tasks_for_file(file_id)
    except Exception as e:
        logger.error(str(e))


    #return summary

def process_one(filename):
    file_id = MDB.get_file_id(filename)
    if file_id == -2:
        pipeline('FM', filename, True, debugging=True)
    else:
        logger.info(f'Already processed:{filename}, {file_id}')
    Notification.send()



def pipeline(instrument, filename, notification_enabled=True, debugging=False):
    """
    single file processing pipeline
    """
    file_id=piepeline_parsing_and_basic_analysis(instrument, filename, notification_enabled, debugging)
    task_manager.run_on_background(pipeline_fits_creation_packets_merging_and_imaging, 'fits-creation-pkt-merging', args=(file_id,))
    #pipeline_fits_creation_packets_merging_and_imaging(file_id)




def process_files(filelist):
    """
    Process files in the given list
    """
    num_processed = 0
    for instrument, files in filelist.items():
        goes.download()
        for filename in files:
            #print('Processing file:', filename)
            pipeline(instrument, filename , True)
            num_processed += 1
    Notification.send()
    #only sending email after all files are processed
    return num_processed





def main():
    flist=find_new_telemetry_files()
    if flist:
        process_files(flist)




if __name__ == '__main__':
    if len(sys.argv) == 1:
        print("""Usage: 
        raw_pipeline <raw telemetry filename>
        """)
    else:
        process_one(sys.argv[1])
