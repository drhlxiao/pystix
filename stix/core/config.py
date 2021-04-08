#!/usr/bin/python3
"""
    stix parser configuration manager
    created on Oct. 20, 2020
"""
import os
import json
from dateutil import parser as dtparser
from stix.core import stix_logger
logger = stix_logger.get_logger()

parser_config = {}


def import_config(namespace, path, filename):
    fname = os.path.join(path, filename)
    with open(fname) as f:
        data = json.load(f)
        parser_config[namespace] = data


def load_config(path='./config'):
    parser_config = {}
    if not os.path.exists(path):
        path= os.path.join(os.path.dirname(__file__),'../../config') 

    fname=os.path.join(path, 'index.json')
    with open(fname) as f:
        data = json.load(f)
        for namespace, filename in data.items():
            import_config(namespace, path, filename)


def config(key):
    return parser_config.get(key, '')


def get_config(key=None):
    # get configuration value
    # For example:  get_config(pipeline.daemon.fits_path)
    if not key:
        return parser_config

    if '.' in key:
        result = parser_config
        try:
            for item in key.split('.'):
                result = result[item]
            return result
        except IndexError or ValueError:
            logger.error(f'Can not find  {key} in config')
            return None
    return parser_config.get(key, '')


def get_idb(utc=None):
    if not utc:
        try:
            return parser_config['idb'][0]['filename']
        except Exception as e:
            logger.error(str(e))
        return ''
    for item in parser_config['idb']:
        dt = dtparser.parse(utc)
        if dt > dtparser.parse(
                item['validity_period'][0]) and dt <= dtparser.parse(
                    item['validity_period'][1]):
            return item['filename']
    return ''


def get_spice(utc=None):
    if not utc:
        try:
            return parser_config['spice'][0]['data']
        except Exception as e:
            logger.error(str(e))
        return []
    for item in parser_config['spice']:
        dt = dtparser.parse(utc)
        if dt > dtparser.parse(
                item['validity_period'][0]) and dt <= dtparser.parse(
                    item['validity_period'][1]):
            return item['data']
    return []


load_config()
#print(config)
#print(get_config('pipeline.mongodb.host'))
#print(get_idb('2020-10-01T00:00:00'))
#print(get_spice('2020-10-01T00:00:00'))
#pprint(config)
