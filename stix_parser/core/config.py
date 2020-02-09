#!/usr/bin/python3
mongodb = {'host': 'localhost', 'user': '', 'password': '', 'port': 27017}
idb = {
    'filename': 'stix_parser/data/idb/idb.sqlite',
}
spice={
        'tls_filename':'stix_parser/data/SPICE/kernels/lsk/naif0012.tls',
        'sclk_filename':'stix_parser/data/SPICE/kernels/sclk/solo_ANC_soc-sclk_20000101_V01.tsc'
        }
deamon={
        'raw_patterns':['/opt/stix/testdata/*ascii', '/home/xiaohl/data/*ascii'],
        'log_path': '/opt/stix/log/'
        #'log_path': '/home/xiaohl/test/'
        }
