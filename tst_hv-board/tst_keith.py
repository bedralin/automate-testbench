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

keith=Keithley_2010("RS232")
id=keith.identification()
print id
print type(id)
time.sleep(1)



#keith.configure("Resistance")
#con=keith.configure
#print con
print "ok man ok man"
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




