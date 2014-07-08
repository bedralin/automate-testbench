#!/usr/bin/env python
#Following command will print documentation of tst_iseg.py:
#pydoc tst_iseg 

"""
OVERVIEW:
Test script to control an Instrument called:
ISEG SHQ226L High Voltage Power Supply

AUTHORS:
Bronson Edralin <bedralin@hawaii.edu>
University of Hawaii at Manoa
Instrumentation Development Lab (IDLab), WAT214
 
HOW TO USE:
sudo python tst_iseg.py
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

iseg=Iseg_SHQ226L("RS232")

# Set Channel
iseg.channel = 2
channel = iseg.channel
print "Channel is: "+channel

# Set Voltage
iseg.set_voltage = 5
set_voltage = iseg.set_voltage
print "Set voltage is: "+set_voltage 




