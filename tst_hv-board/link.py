#!/usr/bin/env python
#Following command will print documentation of link.py:
#pydoc link  

"""
OVERVIEW:
Link Drivers to establish connection
with Instruments

AUTHORS:
Harley Cumming <harleys@hawaii.edu>
Bronson Edralin <bedralin@hawaii.edu>
University of Hawaii at Manoa
Instrumentation Development Lab (IDLab), WAT214

DESCRIPTION:
Ethernet Class used to access Intsrument through GPIB via Ethernet.
RS232 Class used to access Instrument through RS-232 via USB.
"""

import vxi11
from threading import Lock
import time
import serial
import socket
import sys

#Ethernet Class is used to access Intsrument through direct Ethernet port. 
class Ethernet:
    def __init__(self, addr=None):
        self.addr = addr
        self.instr = vxi11.Instrument(addr)
	# Mutex ensures only 1 person access instrument at a time
        self.mutex = Lock()  

#    def connect(self, addr=None):
#        if (addr != None):
#            self.addr = addr
#        if (self.addr != None):
#            instr = vxi11.Instrument(addr)
#        else:
#            raise IOException('No Address Provided')

    # cmd is used for write commands
    def cmd(self,cmd=None):
        self.mutex.acquire()  # User is using it so lock it
        try:
            self.instr.write(cmd)
        finally:
            self.mutex.release()  # User is done so unlock it

    # ask used for reading value/string from instrument
    def ask(self, cmd=None):
        self.mutex.acquire()
        result = None
        try:
            result = self.instr.ask(cmd)  
        finally:
            self.mutex.release()
            return result  

    # ask_print used for printing value/string from instrument
    def ask_print(self, cmd=None):
        self.mutex.acquire()
        try:
            print(self.instr.ask(cmd))
        finally:
            self.mutex.release()


# Ethernet_Controller class used to access Instrument through GPIB via Ethernet
class Ethernet_Controller:
    def __init__(self, addr=None, port=None):
	self.addr = str(addr)    
	self.mutex = Lock()
	self.delay = 0
	self.timeout = 0.5
	try:
	    self.port = int(port)
	except TypeError:
	    print "Type Error for port #" + str(port) + ". Should be int."
	try:
	    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	except socket.error:
	    print 'Failed to create socket!'
	    sys.exit()
	print "Socket Created Successfully..."
	self.sock.settimeout(self.timeout)
        try:
            self.sock.connect((self.addr, self.port))
        except TypeError:
            print "Socket Failed to Connect to IP (" + self.addr + \
            ") with port #" + str(self.port) + "."
            print "Type Error!\n"
            sys.exit()
        except socket.error:
            print "Socket Failed to Connect to IP (" + self.addr + \
            ") with port #" + str(self.port) + "."
            print "Socket Error!\n"
            sys.exit()
	print "Socket Connected to IP (" + self.addr + \
	") with port #" + str(self.port) + ".\n"

    def sock_timeout(self, timeout=0.5):
	self.timeout = timeout
	self.sock.settimeout(self.timeout)
	print "Socket timeout set to: " + str(self.timeout) + "secs"

    def sock_close(self):
	self.sock.close()
	print "Socket is now closed"

    # cmd is used for write commands
    def cmd(self,cmd=None):
        self.mutex.acquire()  # User is using it so lock it
	print "cmd started"
	"""
	try:
	    self.sock.connect((self.addr, self.port))
	except TypeError:
	    print "Socket Failed to Connect to IP (" + self.addr + ") with port #"\
	    + str(self.port) + "."
	    print "\nType Error!"
	    sys.exit()
	except socket.error:
	    print "Socket Failed to Connect to IP (" + self.addr + ") with port #"\
	    + str(self.port) + "."
	    print "\nSocket Error!"
	    sys.exit()
	"""
        try:
            self.sock.send(str(cmd)+"\r\n\r\n")
            time.sleep(self.delay)
	except socket.error:
	    print "Send failed!"
        finally:
	    #self.sock.close()
	    print "cmd"
            self.mutex.release()  # User is done so unlock it

    # ask used for reading value/string from instrument
    def ask(self, cmd=None):
        self.mutex.acquire()  # User is using it so lock it
	self.result = None
	print "ask started"
	"""
        try:
            self.sock.connect((self.addr, self.port))
        except TypeError:
            print "Socket Failed to Connect to IP (" + self.addr + \
	    ") with port #" + str(self.port) + "."
            print "\nType Error!"
	    sys.exit()
        except socket.error:
            print "Socket Failed to Connect to IP (" + self.addr + \
	    ") with port #" + str(self.port) + "."
	    print "\nSocket Error!"
            sys.exit()
	"""
        try:
            self.sock.send(str(cmd)+"\r\n\r\n")
	    time.sleep(self.delay)
        except socket.error:
            print "Send failed"
        finally:
	    self.result = self.sock.recv(100)
	    #self.sock.close()
	    print "ask"
            self.mutex.release()  # User is done so unlock it
	    return self.result
	
    # ask_print used for printing value/string from instrument
    def ask_print(self, cmd=None):
        self.mutex.acquire()  # User is using it so lock it
        self.result = None
        try:
            self.sock.connect((self.addr, self.port))
        except TypeError:
            print "Socket Failed to Connect to IP (" + self.addr + \
	    ") with port #" + str(self.port) + "."
            print "\nType Error!"
            sys.exit()
        except socket.error:
            print "Socket Failed to Connect to IP (" + self.addr + \
	    ") with port #" + str(self.port) + "."
            print "\nSocket Error!"
            sys.exit()
        try:
            self.sock.send(str(cmd)+"\r\n\r\n")
            time.sleep(self.delay)
        except socket.error:
            print "Send failed!"
        finally:
            self.result = self.sock.recv(100)
	    self.sock.close()
            self.mutex.release()  # User is done so unlock it
	    print self.result
            return self.result


#RS232 Class is used to access Instrument through RS-232 via USB.
class RS232:
    def __init__(self,port='/dev/ttyUSB0',baudrate=9600,databits=8, \
		parity='None',stopbits=1,timeout=0.525,xonxoff=False,rtscts=False):
	self.port = port  # Device name or port #
	self.baudrate = int(baudrate)  # Baud rate such as 9600
	self.databits = int(databits)  # Number of databits such as 5,6,7,8
	parity=parity.upper()  # Enable parity checking: None,Even,Odd,Even,etc.
	if parity == 'NONE':
	    self.parity=serial.PARITY_NONE
	elif parity == 'EVEN':
	    self.parity=serial.PARITY_EVEN
        elif parity == 'ODD':
            self.parity=serial.PARITY_ODD
        elif parity == 'MARK':
            self.parity=serial.PARITY_MARK
        elif parity == 'SPACE':
            self.parity=serial.PARITY_SPACE
	else:
	    print "Invalid Parity: ",parity
	self.stopbits = int(stopbits)  # Numb of stop bits such as 1,1.5,2
	self.timeout = float(timeout)    # Set read timeout
	self.xonxoff = xonxoff  # Enable software flow control: True/False
	self.rtscts = rtscts  # Enable hardware (RTS/CTS) flow control: True/False

        #Open the serial port
        self.ser=serial.Serial(
            port = self.port,
            baudrate = self.baudrate,
            parity = self.parity,
            stopbits = self.stopbits,
            bytesize = self.databits
        )
        self.ser.xonxoff = self.xonxoff
        self.ser.rtscts = self.rtscts
	self.ser.close()

    def cmd(self,cmd=None):
	"""
	#Open the serial port
	ser=serial.Serial(
            port = self.port,
            baudrate = self.baudrate,
            parity = self.parity,
            stopbits = self.stopbits,
            bytesize = self.databits        
	)	

	ser.xonxoff = self.xonxoff
	ser.rtscts = self.rtscts
	"""
	self.ser.open()
	self.ser.isOpen()
        #send cmd to device
        #Note: \r\n carriage return and line feed to characters
        #       This is requested by some devices like the 
	#	ISEG SHQ226L HV Power Supply
	self.ser.write(cmd + '\r\n')
	self.ser.close()  #Close Serial port

    def ask(self,cmd=None):
	"""
        #Open the serial port
        ser=serial.Serial(
            port = self.port,
            baudrate = self.baudrate,
            parity = self.parity,
            stopbits = self.stopbits,
            bytesize = self.databits
        )
        ser.xonxoff = self.xonxoff
        ser.rtscts = self.rtscts
	"""
	self.ser.open()
        self.ser.isOpen()
        #send cmd to device
        #Note: \r\n carriage return and line feed to characters
        #       This is requested by some devices like the
	#	ISEG SHQ226L HV Power Supply
        self.ser.write(cmd + '\r\n')
	result=''
	time.sleep(self.timeout)  #Wait for response from device
	while self.ser.inWaiting() > 0:
	    result += self.ser.read(1)
        self.ser.close()   #Close Serial port
	if result != '':
	    return result
	else:
            print "There was no feedback from device!"

    def ask_print(self,cmd=None):
	"""
        #Open the serial port
        ser=serial.Serial(
            port = self.port,
            baudrate = self.baudrate,
            parity = self.parity,
            stopbits = self.stopbits,
            bytesize = self.databits
        )        
	ser.xonxoff = self.xonxoff
        ser.rtscts = self.rtscts
	"""
        self.ser.open()
	self.ser.isOpen()
	#send cmd to device
	#Note: \r\n carriage return and line feed to characters
	#	This is requested by some devices like the 
	#	ISEG SHQ226L HV Power Supply
        self.ser.write(cmd + '\r\n')
        result=''
        time.sleep(self.timeout)   #Wait for response from device
        while self.ser.inWaiting() > 0:
            result += self.ser.read(1)
        self.ser.close()   #Close Serial port
	if result != '':
	    print result
	else:
	    print "There was no feedback from device!"
        return result


