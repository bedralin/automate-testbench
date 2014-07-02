import csv
import math
import datetime
import subprocess
from collections import *
from link import * 
from channel import Channel
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




