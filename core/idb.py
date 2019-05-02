#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @title        : IDB.py
# @description  : stix idb python interface
# @author       : Hualin Xiao
# @date         : Feb. 15, 2019
from __future__ import (absolute_import, unicode_literals)

import pprint
import sqlite3
from core import stix_logger

LOGGER = stix_logger.LOGGER
STIX_IDB_FILENAME='idb/idb.sqlite'

class IDB(object):
    def __init__(self, filename=STIX_IDB_FILENAME, logger=LOGGER):
        self.filename = filename
        self.conn = None
        self.parameter_structures=dict()
        self.soc_descriptions=dict()
        self.s2k_table_contents=dict()
        self.connect_database(filename)
        self.logger=logger

    def connect_database(self,filename):
        try:
            self.conn = sqlite3.connect(filename,check_same_thread=False)
        except sqlite3.Error as er:
            self.logger.error(er.message)
            raise Exception('Failed to connect to IDB !')
        else:
            self.cur = self.conn.cursor()

    def __del__(self):
        if self.conn:
            self.conn.close()

    def execute(self, sql,arguments, result_type='list'):
        """
        execute sql and return results in a list or a dictionary
        Args:
            sql: sql
            result_type: type of results. It can be list or dict
        return:
            database query result
        N
        """
        if not self.cur:
            raise Exception('IDB is not initialized!')
        else:
            rows = None
            if arguments:
                self.cur.execute(sql,arguments)
            else:
                self.cur.execute(sql)

            if result_type == 'list':
                rows = self.cur.fetchall()
            else:
                rows = [
                    dict(
                        zip([column[0]
                             for column in self.cur.description], row))
                    for row in self.cur.fetchall()
                ]
            return rows

    def get_spid_info(self, spid):
        """ get SPID description """
        sql='select PID_DESCR,PID_TYPE,PID_STYPE from PID where PID_SPID=? limit 1'
        return self.execute(sql,(spid,))
    
    def get_scos_description(self, name):
        """ get scos long description """
        if name in self.soc_descriptions:
            return self.soc_descriptions[name]
        else:
            rows = self.execute(
                'select SW_DESCR from sw_para where scos_name=? ',(name,))
            if rows:
                res=rows[0][0]
                self.soc_descriptions[name]=res
                return res
            return 'NO_SCOS_DESC'

    def get_telemetry_description(self, spid):
        """get telemetry data information """
        sql=('select sw_para.SW_DESCR, tpcf.tpcf_name  '
            ' from sw_para join tpcf '
            'on tpcf.tpcf_name=sw_para.scos_name and tpcf.tpcf_spid= ?')
        return self.execute(sql,(spid,))

    def get_packet_type_offset(self, packet_type, packet_subtype):
        sql = ('select PIC_PI1_OFF, PIC_PI1_WID from PIC '
               'where PIC_TYPE=? and PIC_STYPE=? limit 1')
        args=(packet_type, packet_subtype)
        rows = self.execute(sql,args)
        if rows:
            return rows[0]
        return 0,0
    def get_PCF_description(self,name):
        sql=('select PCF_DESCR from PCF where PCF_NAME=?')

        return self.execute(sql,(name,))


    def get_packet_type_info(self, packet_type, packet_subtype, pi1_val=-1):
        """
        Identify packet type using service, service subtype and information in IDB table PID
        """
        args=None
        if pi1_val == -1:
            sql = ('select PID_SPID, PID_DESCR, PID_TPSD from PID '
                   'where PID_TYPE=? and PID_STYPE=? limit 1')
            args=(packet_type, packet_subtype)
        else:
            sql = (
                'select PID_SPID, PID_DESCR, PID_TPSD from PID '
                'where PID_TYPE=? and PID_STYPE=? and PID_PI1_VAL=? limit 1'
            )
            args=(packet_type, packet_subtype, pi1_val)
        rows = self.execute(sql, args, 'dict')
        return rows[0]

    def get_s2k_parameter_types(self, ptc, pfc):
        """ get parameter type """
        if (ptc,pfc) in self.s2k_table_contents:
            return self.s2k_table_contents[(ptc,pfc)]
        else:
            sql = ('select S2K_TYPE, LENGTH, S2K_TYPE_Description from '
                   ' tblConfigS2KParameterTypes where PTC = ? '
                   ' and ? >= PFC_LB and  PFC_UB >= ? limit 1')
            args=(ptc, pfc, pfc)
            rows = self.execute(sql, args, 'dict')
            self.s2k_table_contents[(ptc,pfc)]=rows[0]
            return rows[0]

    def convert_NIXG_NIXD(self, name):
        sql = (
            'select PDI_GLOBAL, PDI_DETAIL, PDI_OFFSET from PDI where PDI_GLOBAL=? '
        )
        args=(name,)
        rows = self.execute(sql, args, 'dict')
        return rows

    def get_fixed_packet_structure(self, spid):
        """
        get parameter structures using SCO ICD (page 39)
        Args:
            spid: SPID
        Returns:
            is_fixed: whether it is a fixed length packet
            parameter structures
         """
        if spid in self.parameter_structures:
            #database query is slower
            return self.parameter_structures[spid]
        else:
            sql = ('select PLF.*, PCF.* '
                   ' from PLF   inner join PCF  on PLF.PLF_NAME = PCF.PCF_NAME '
                   ' and PLF.PLF_SPID=? order by PLF.PLF_OFFBY asc')
            args=(spid,)
            res=self.execute(sql, args, 'dict')
            self.parameter_structures[spid]=res
            return res

    def get_telecommand_characteristics(self, service_type, service_subtype, command_subtype=-1):
        """
          command subtype is only used for 237, 7
        """
        sql=('select * from CCF where CCF_TYPE=? and CCF_STYPE =? order by CCF_CNAME asc')
        res=self.execute(sql, (service_type,service_subtype) , 'dict')
        if command_subtype>=0 and len(res)>1:
            #for TC(237,7) , ZIX37701 -- ZIX37724
            #source_id in the header is needed to identify the packet type
            return res[command_subtype-1]
        else:
            return res[0]
    def get_telecommand_parameters(self,name):
        sql='select * from CDF where CDF_CNAME=?'
        args=(name,)
        res=self.execute(sql, args, 'dict')
        return res

    def get_variable_packet_structure(self, spid):
        if spid in self.parameter_structures:
            return self.parameter_structures[spid]
        else:
            sql = (
                'select VPD.*, PCF.*'
                ' from VPD inner join PCF on  VPD.VPD_NAME=PCF.PCF_NAME and VPD.VPD_TPSD=? order by '
                ' VPD.VPD_POS asc')
            res=self.execute(sql, (spid,), 'dict')
            self.parameter_structures[spid]=res
            return res



STIX_IDB = IDB()

def test():
    """ test  the database interfaces"""
    #print(STIX_IDB.get_s2k_parameter_types(3, 16))
    #print(STIX_IDB.get_parameter_physical_value('CIXP0024TM', 2405))
    #print(STIX_IDB.get_parameter_physical_value('CIX00036TM', 20))
    #for i in range(100000):
    #    a=STIX_IDB.get_s2k_parameter_types(3, 16)
    #pprint.pprint(STIX_IDB.get_telecommand_characteristics(237, 7,1))
    #pprint.pprint(STIX_IDB.get_telecommand_characteristics(237, 7,2))
    pprint.pprint(STIX_IDB.get_variable_packet_structure(54137))


if __name__ == '__main__':
    test()
