#!/usr/bin/env python
#Following command will print documentation of iseg_SHQ226L.py:
#pydoc iseg_SHQ226L 

"""
OVERVIEW:
Python wrapper for commands to control an Instrument called:
ISEG SHQ226L High Voltage Power Supply

AUTHORS:
Bronson Edralin <bedralin@hawaii.edu>
University of Hawaii at Manoa
Instrumentation Development Lab (IDLab), WAT214
 
HOW TO USE:
"from iseg_SHQ226L.py import Iseg_SHQ226L" will import the class
"iseg = Iseg_SHQ226L(addr)" will create the instrument object
"iseg.channel = 2" will set channel to chan 2 (IMPORTANT: Set chan 1st)
"iseg.set_voltage = 5" will set voltage to 5 Volts on channel 2
"print iseg.set_voltage" will read the set voltage on chan 2
"print iseg.actual_voltage" will read the actual voltage on chan 2
"""

from link import * 

class Iseg_SHQ226L(object):
    def __init__(self, addr=None):
	addr=addr.upper()
	#Set up link connection. Either RS232 via USB or GPIO via Ethernet
	if (addr == 'RS232') or (addr == 'RS-232'):
	    self.link = RS232()
	elif (addr != None):
	    self.link = Ethernet(addr)
	else:
	    print "Invalid address: "+str(addr)

    def __binary_cmd__(self, cmd):
        if isinstance(cmd, str):  #If cmd is a string
            cmd = cmd.upper()     
        try:  
	    # Binary cmd must be one of these and be converted into string
            cmd={1:'1','1':'1',0:'0','0':'0','ON':'1','OFF':'0'}[cmd]
        except KeyError:
            print "Invalid operation: "+str(cmd)  # If Binary cmd was not on list
        else:
	    #print cmd   # Uncomment for debug
            return str(cmd)

    #Channels 1-8
    @property
    def channel(self):
        #print self.chan  # Uncomment for debug
        #self.chan=1
        return str(self.chan)

    @channel.setter
    def channel(self,chan):
        valid_channels=[1,2,3,4,5,6,7,8]
        try:
            chan = int(chan)
            self.chan = str(valid_channels[valid_channels.index(chan)])
        except ValueError:
            print "Invalid Channel Number: "+str(chan)+". Channels 1-8 only."

    # Read module identifier
    # nnnn	;n.nn		;U	    ;I*
    # (unit #	;software rel.	;V_outmax   ;I_outmax)
    @property
    def module_identifier(self):
        #print ("#")  #Uncomment for debug
        #self.link.ask_print("#")  # Print Instrument's Resp
        return str(self.link.ask("#"))

    # Read break time
    # (break time 0 ... 255 ms)
    @property
    def break_time(self):
        #print ("W")  #Uncomment for debug
        #self.link.ask_print("W")  # Print Instrument's Resp
        return str(self.link.ask("W"))

    # Write break time
    # (break time 0 ... 255 ms)
    @break_time.setter
    def break_time(self, cmd):
        try:
            cmd = float(cmd)
            if cmd >= 0 and cmd <= 255:
                #print ("W"+"="+str(cmd))  #Uncomment for debug
                self.link.cmd("W"+"="+str(cmd))
            else:
                print "Invalid Break Time Value: "+str(cmd)+\
                " (ms). Break Time Range: 0-255 ms"
        except ValueError:
            print "Invalid Break Time Value: "+str(cmd)+\
            " (ms). Break Time Range: 0-255 ms"

    # Read actual voltage (V) on channel
    # {polarity/mantisse/exp. with sign}      (in V)
    @property
    def actual_voltage(self):
        #print ("U"+self.chan)  #Uncomment for debug
        #self.link.ask_print("U"+self.chan)  # Print Instrument's Resp  
        return str(self.link.ask("U"+self.chan))

    # Read actual current (A) on channel
    # {mantisse/exp. with sign}	    (in A) 
    @property
    def actual_current(self):
        #print ("I"+self.chan)  #Uncomment for debug
        #self.link.ask_print("I"+self.chan)  # Print Instrument's Resp  
        return str(self.link.ask("I"+self.chan))

    # Read voltage limit on channel
    # (in % of V_outmax) 
    @property
    def voltage_limit(self):
        #print ("M"+self.chan)  #Uncomment for debug
        #self.link.ask_print("M"+self.chan)  # Print Instrument's Resp  
        return str(self.link.ask("M"+self.chan))

    # Read current limit on channel
    # (in % of I_outmax) 
    @property
    def current_limit(self):
        #print ("N"+self.chan)  #Uncomment for debug
        #self.link.ask_print("N"+self.chan)  # Print Instrument's Resp  
        return str(self.link.ask("N"+self.chan))

    # Read set voltage on channel
    # {mantisse/exp. with sign}     (in V) 
    @property
    def set_voltage(self):
	#print ("D"+self.chan)  #Uncomment for debug
	#self.link.ask_print("D"+self.chan)  # Print Instrument's Resp    
        return str(self.link.ask("D"+self.chan))

    # Write set voltage on channeli
    # (voltage correspondig resolution in V; <M1)
    @set_voltage.setter
    def set_voltage(self, cmd):
        try:
            cmd = float(cmd)
        except ValueError:
            print "Invalid Set Voltage Value: "+str(cmd)
        else:
            #print ("D"+self.chan+"="+str(cmd))  #Uncomment for debug
            self.link.cmd("D"+self.chan+"="+str(cmd))

    # Read ramp speed on channel 
    # (2 ... 255 V/s)
    @property
    def ramp_speed(self):
        #print ("V"+self.chan)  #Uncomment for debug
	#self.link.ask_print("V"+self.chan)  # Print Instrument's Resp
        return str(self.link.ask("V"+self.chan))

    # Write ramp speed on channel
    # (ramp speed = 2 - 255 V/s)
    @ramp_speed.setter
    def ramp_speed(self, cmd):
        try:
            cmd = float(cmd)
            if cmd >= 2 and cmd <= 255:
                #print ("V"+self.chan+"="+str(cmd))  #Uncomment for debug
                self.link.cmd("V"+self.chan+"="+str(cmd))
            else:
                print "Invalid Break Time Value: "+str(cmd)+\
                " (V/s). Ramp Speed Range: 2-255 V/s"
        except ValueError:
            print "Invalid Break Time Value: "+str(cmd)+\
            " (V/s). Ramp Speed Range: 2-255 V/s"

    # Read current trip on channel 
    # (trip corresponding resolution Range: A>0) 
    @property
    def current_trip_A(self):
        #print ("L"+self.channel)  #Uncomment for debug
        #self.link.ask_print("L"+self.chan)  # Print Instrument's Resp
        return str(self.link.ask("L"+self.chan))

    # Write current trip on channel  (Range: A)
    @current_trip_A.setter
    def current_trip_A(self, cmd):
        try:
            cmd = int(cmd)
        except ValueError:
            print "Invalid Current (A) Trip Value: "+str(cmd)
        else:
            #print ("L"+self.chan+"="+str(cmd))  #Uncomment for debug  
            self.link.cmd("L"+self.chan+"="+str(cmd))

    # Read current trip on channel 
    # (trip corresponding resolution Range: mA>0) 
    @property
    def current_trip_mA(self):
        #print ("LB"+self.chan)  #Uncomment for debug
        #self.link.ask_print("LB"+self.chan)  # Print Instrument's Resp
        return str(self.link.ask("LB"+self.chan))

    # Write current trip on channel (Range: mA)
    @current_trip_mA.setter
    def current_trip_mA(self, cmd):
        try:
            cmd = int(cmd)
        except ValueError:
            print "Invalid Current (mA) Trip Value: "+str(cmd)
        else:
            #print ("LB"+self.chan+"="+str(cmd))  #Uncomment for debug  
            self.link.cmd("LB"+self.chan+"="+str(cmd))

    # Read current trip on channel 
    # (trip corresponding resolution Range: uA>0) 
    @property
    def current_trip_uA(self):
        #print ("LS"+self.chan)  #Uncomment for debug
        #self.link.ask_print("LS"+self.chan)  # Print Instrument's Resp
        return str(self.link.ask("LS"+self.chan))

    # Write current trip on channel (Range: uA)
    @current_trip_uA.setter
    def current_trip_uA(self, cmd):
        try:
            cmd = int(cmd)
        except ValueError:
            print "Invalid Current (uA) Trip Value: "+str(cmd)
        else:
            #print ("LS"+self.chan+"="+str(cmd))  #Uncomment for debug  
            self.link.cmd("LS"+self.chan+"="+str(cmd))

    # Read auto start on channel
    # (conditions => Auto start)
    @property
    def auto_start(self):
        #print ("A"+self.chan)  #Uncomment for debug
        #self.link.ask_print("A"+self.chan)  # Print Instrument's Resp
        return str(self.link.ask("A"+self.chan))

    # Write auto start on channel 
    @auto_start.setter
    def auto_start(self, cmd):
        try:
            cmd = int(cmd)
        except ValueError:
            print "Invalid Auto Start Value: "+str(cmd)
        else:
            #print ("A"+self.chan+"="+str(cmd))  #Uncomment for debug 
            self.link.cmd("A"+self.chan+"="+str(cmd))

    # Read status information
    @property
    def status_word(self):
        #print ("S"+self.chan)  #Uncomment for debug
        #self.link.ask_print("S"+self.chan)  # Print Instrument's Resp
        return str(self.link.ask("S"+self.chan))

    # Read module status information 
    # (code 0...255, => Module Status)
    @property
    def module_status(self):
        #print ("T"+self.chan)  #Uncomment for debug
        #self.link.ask_print("T"+self.chan)  # Print Instrument's Resp
        return str(self.link.ask("T"+self.chan))



