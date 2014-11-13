#!/usr/bin/env python
'''
This script is a database utility for IDLab.
'''

import datetime
import time
import os
import psycopg2
import logging
import csv
import hvb_db_utility
import db_utility

__author__ = "Bronson Edralin"
__copyright__ = "Copyright 2014 Instrumentation Development Laboratory (IDLab), Department of Physics, University of Hawaii at Manoa"
__credits__ = ["Bronson Edralin","Christian A. Damo", "Reed Shinsato"]
__version__ = "0.01"
__maintainer__ = "Bronson Edralin"
__email__ = "bedralin@hawaii.edu"
__status__ = "Prototype"

logging.basicConfig(filename='IDLAB_log',level=logging.DEBUG,format='%(asctime)s %(message)s')

db=hvb_db_utility.DatabaseUtility()

#check_table=db.check_table_exists("mytable")


#db.create_table("WOW")
db.create_table("HVB_RawTest")

#db.insert_data_into_database("BARCODENUM_hvb_test_raw_r1BE.csv","HVB_RawTest")
db.close_conn()

