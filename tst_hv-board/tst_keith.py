#!/usr/bin/env python
#Following command will print documentation of tst_keith.py:
#pydoc tst_keith

"""
OVERVIEW:
Test script to control an Instrument called:
Keithley 2010 Multimeter

AUTHORS:
Bronson Edralin <bedralin@hawaii.edu>
University of Hawaii at Manoa
Instrumentation Development Lab (IDLab), WAT214
 
HOW TO USE:
sudo python tst_keith.py
"""

import csv
import math
import datetime
import subprocess
from collections import *
from link import * 
from threading import Lock
from keithley_2010 import *
import vxi11
import time
import math
import os
import serial

#b=RS232()
#b.ask_print("*IDN?")

keith=Keithley_2010("192.168.1.102",1234)
id=keith.identification()
print id
print type(id)
keith.Check_Error()
#time.sleep(1)

id=keith.identification()
print id
print type(id)
#time.sleep(1)
keith.Check_Error()
#keith.reset()
#time.sleep(1)

voltage_unit = keith.voltage_unit
print voltage_unit
keith.Check_Error()

voltage_unit = keith.voltage_unit
print voltage_unit
keith.Check_Error()

"""
#keith.configure("Resistance")
#con=keith.configure
#print con
print "ok man ok man"
#keith.configure_voltage="dc"
con=keith.configure
#time.sleep(1)
print "This should be voltage DC: "+str(con)

checkError = keith.Check_Error()
print checkError
keith.configure="resistance"
#time.sleep(1)
con=keith.configure
print "This should be resistance: "+str(con)
keith.configure_voltage="dc"
con=keith.configure
#time.sleep(1)
print "This should be voltage DC: "+str(con)
keith.configure_current="DC"
con=keith.configure
#time.sleep(1)
print "This should be current DC: "+str(con)

keith.configure_voltage="dc"
con=keith.configure
#time.sleep(1)
print "This should be voltage DC: "+str(con)

keith.configure="resistance"
#time.sleep(1)
con=keith.configure
print "This should be resistance: "+str(con)
keith.configure_voltage="dc"
con=keith.configure
#time.sleep(1)
print "This should be voltage DC: "+str(con)
keith.configure_current="DC"
con=keith.configure
#time.sleep(1)
print "This should be current DC: "+str(con)

keith.configure_voltage="dc"
con=keith.configure
#time.sleep(1)
print "This should be voltage DC: "+str(con)

keith.configure="resistance"
#time.sleep(1)
con=keith.configure
print "This should be resistance: "+str(con)
keith.configure_voltage="dc"
con=keith.configure
#time.sleep(1)
print "This should be voltage DC: "+str(con)
keith.configure_current="DC"
con=keith.configure
#time.sleep(1)
print "This should be current DC: "+str(con)
"""



