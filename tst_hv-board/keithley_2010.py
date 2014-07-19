#!/usr/bin/env python
#Following command will print documentation of keithley_2010.py:
#pydoc keithley_2010 

"""
OVERVIEW:
Python wrapper for commands to control an Instrument called:
Keithley 2010 Multimeter

AUTHORS:
Bronson Edralin <bedralin@hawaii.edu>
University of Hawaii at Manoa
Instrumentation Development Lab (IDLab), WAT214
 
HOW TO USE:
"from keithley_2010.py import Keithley_2010" will import the class
"keithley = Keithley_2010(addr)" will create the instrument object
"keithley.channel = 2" will set channel to chan 2 (IMPORTANT: Set chan 1st)
"keithley.set_voltage = 5" will set voltage to 5 Volts on channel 2
"print keithley.set_voltage" will read the set voltage on chan 2
"""

from link import *

class Keithley_2010(object):
    def __init__(self, addr=None,port=None):
        addr=addr.upper()
        #Set up link connection. Either RS232 via USB or GPIO via Ethernet
        if (addr == 'RS232') or (addr == 'RS-232'):
            self.link = RS232()
        elif (addr != None) and (port == None):
            self.link = Ethernet(addr)
	elif (addr != None) and (port != None):
	    self.link = Ethernet_Controller(addr,port)
        else:
            print "Invalid address: "+str(addr)

    def __binary_cmd__(self, cmd):
        if isinstance(cmd, str):  #If cmd is a string
            cmd = cmd.upper()
        try:
            # Binary cmd must be one of these and be converted into string
            cmd={1:'1','1':'1',0:'0','0':'0','ON':'1','OFF':'0'}[cmd]
        except KeyError:
            print "Invalid operation: "+cmd  # If Binary cmd was not on list
        else:
            #print cmd   # Uncomment for debug
            return cmd

    def reset(self):
        self.link.cmd("*RST")
        #self.link.cmd("*CLS")

    # *IDN? - Identification Query: Read identification code
    def identification(self):
	return self.link.ask("*IDN?")

    def self_test_query(self):
	return self.link.ask("*TST?")

    def Check_Error(self):
	error_numb,error = self.link.ask("SYST:ERR?").split(',')
	if (error_numb != "0") and (error_numb != "-420"):
	    print "Error has occured: "+error_numb+", "+error
	    return "Error has occured: "+error_numb+", "+error
	elif (error_numb == "-420"):
            print "Error has occured: "+error_numb+", "+error
            return "Error has occured: "+error_numb+", "+error    
    # SCPI signal oriented measurement commands
    @property
    def configure(self):
	return self.link.ask(":CONFigure?")

    @configure.setter
    def configure(self,function):
	valid_set = {'CURRENT','VOLTAGE','RESISTANCE','FRESISTANCE',\
	'PERIOD','FREQUENCY','TEMPERATURE','DIODE','CONTINUITY'}
	function = function.upper()
	if function not in valid_set:
	    raise ValueError("Invalid Configuration")
	else:
	    self.link.cmd("CONFigure:"+function)	

    @property
    def configure_voltage(self):
        return self.link.ask(":CONFigure?")

    @configure_voltage.setter
    def configure_voltage(self,acdc):
        valid_set = {'AC','DC'}
        acdc = acdc.upper()
        if (acdc not in valid_set):
            raise ValueError("Invalid Configuration of Voltage")
        else:
            self.link.cmd("CONFigure:VOLTage:"+acdc)   
 
    @property
    def configure_current(self):
        return self.link.ask(":CONFigure?")

    @configure_current.setter
    def configure_current(self,acdc):
        valid_set = {'AC','DC'}      
        acdc = acdc.upper()
        if (acdc not in valid_set):
            raise ValueError("Invalid Configuration of Current")
        else:
            self.link.cmd("CONFigure:CURRent:"+acdc)   

    @property
    def voltage_unit(self):
        return self.link.ask(":UNIT:VOLTage:AC?")

    @voltage_unit.setter
    def voltage_unit(self, unit):
        valid_set = {'VPP','VRMS','DBM'}
        unit = unit.upper()
        if unit not in valid_set:
            raise ValueError("Invalid units for voltage")
        else:
            self.link.cmd("VOLTage:UNIT "+unit)

