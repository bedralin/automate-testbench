#/usr/bin/env python
#Following command will print documentation of hvb_assembly_autotest.py:
#pydoc hvb_assembly_autotest 

"""
AUTHORS:
Bronson Edralin <bedralin@hawaii.edu>
University of Hawaii at Manoa
Instrumentation Development Lab (IDLab), WAT214

HVB ASSEMBLY TEST TEAM:
SOFTWARE = Bronson Edralin <bedralin@hawaii.edu>
HARDWARE = James Bynes <bynes@hawaii.edu>
MENTOR = Gerard Visser <gvisser@indiana.edu>

OVERVIEW:
This is an automated test written to test the HVB Assembly Boards. There should be around 90 of these up for testing. Just run this script on Raspberry Pi (RPi) and it will generate a csv file of the raw results in the Raspberry Pi location /home/pi/daqtest1 which points to daqtest1.iucf.indiana.edu:/home/gvisser/BelleII/hvbtest/export because of nfs mount. You can see the nfs mount settings in the Raspberry Pi location /etc/fstab file. Mount is automatically performed on reboot by editing /etc/rc.local file and putting: mount -o nolock /home/pi/daqtest1 

INSTRUMENTS USED:
ISEG SHQ226L High Voltage Power Supply
KEITHLEY 2010 Multimeter
 
HOW TO RUN:
python main.py
"""

from hvb_assembly_autotest import *
import sys
import datetime

MULTIMETER_ADDR = "192.168.1.102"
HV_SUPPLY_ADDR = "RS232"
ISEG_VOLTAGE = "1000"
TIME_PERIOD = "0.2"
PURPOSE = "HVB_RawTest"
LOC_DIR_FOR_STORING_CSV = "/home/pi/daqtest1/"
#LOC_DIR_FOR_STORING_CSV = "/home/bronson/"

# Note: CSV File saved in /home/pi/daqtest1

print "\nWelcome to Automated Test for HVB Assemblies for the Belle II Detector System\n"
print "Collaboration between:"
print "\tIDLab from University of Hawaii"
print "\tUniversity of Indiana\n"
print "TEAM:"
print "\tSOFTWARE: Bronson Edralin <bedralin@hawaii.edu>"
print "\tHARDWARE: James Bynes <bynes@hawaii.edu>"
print "\tMENTOR: Gerard Visser <gvisser@indiana.edu>\n"

print "Recommended voltage for test using unpotted boards is 1kV, and 4kV after potted. If you want to change this parameter setting or anything else, please do so in main.py\n"
print "Current Parameters are:"
print "\t>> Keithley Mult Addr = "+MULTIMETER_ADDR
print "\t>> ISEG HV Supply Addr = "+HV_SUPPLY_ADDR
print "\t>> ISEG Voltage = "+ISEG_VOLTAGE
print "\t>> TIME PERIOD(s) for Switching = "+TIME_PERIOD+" sec"
print "\t>> PURPOSE = "+PURPOSE
print "\t>> CSV file will be stored in: "+LOC_DIR_FOR_STORING_CSV
print "\n"

SERIAL_NUMBER = raw_input("Please enter serial number of board: ")
SERIAL_NUMBER = str(SERIAL_NUMBER)

print "\nStarting Automated Test for HVB Assembly with Serial #"+SERIAL_NUMBER+" Now!!!\n"

# START TEST
hvb_assembly_test(MULTIMETER_ADDR,HV_SUPPLY_ADDR,\
    SERIAL_NUMBER,ISEG_VOLTAGE,TIME_PERIOD,PURPOSE,LOC_DIR_FOR_STORING_CSV)

