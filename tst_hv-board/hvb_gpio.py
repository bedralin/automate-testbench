import RPi.GPIO as GPIO
import time

NO=False
YES=True
DELAY=1

# GPIO.BOARD option specifies that you are referring to pins by the number
# of the pin the plug ex. See middle
GPIO.setmode(GPIO.BOARD)  

# GPIO.BCM option means that you are referring to pins by the
# "Broadcom SOC channel" number, these are the numbers after "GPIO"
# in the green rectangles around the outside of the diagrams
# Refer to http://raspberrypi.stackexchange.com/questions/12966/what-is-the-difference-between-board-and-bcm-for-gpio-pin-numbering
# GPIO.setmode(GPIO.BCM)

# Initialize Past states for GPIO
A_STATE_MINUS=False  # GPIO18 is Pin12
B_STATE_MINUS=False  # GPIO22 is Pin15
C_STATE_MINUS=False  # GPIO23 is Pin16
A_BOARD_SELECT_MINUS=False  # GPIO24 is Pin18
B_BOARD_SELECT_MINUS=False  # GPIO25 is Pin22
C_BOARD_SELECT_MINUS=False  # GPIO27 is Pin13
A_RAS_MINUS=False  # GPIO4 is Pin7
B_RAS_MINUS=False  # GPIO17 is Pin11


#GPIO.setmode(GPIO.BOARD) ## Use board pin numbering

# Declare outputs for GPIO Pins
GPIO.setup(12, GPIO.OUT)
GPIO.setup(15, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(13, GPIO.OUT)    
GPIO.setup(7, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)

# 2nd Column of 5 LED lights left of board
def mux_relays(C,B,A):
    # GPIO18 is Pin12
    # GPIO22 is Pin15
    # GPIO23 is Pin16
    #GPIO.setup(12, GPIO.OUT)
    #GPIO.setup(15, GPIO.OUT)
    #GPIO.setup(16, GPIO.OUT)
    global A_STATE_MINUS
    global B_STATE_MINUS
    global C_STATE_MINUS

    if (A!=A_STATE_MINUS):
	GPIO.output(12, A)
    if (B!=B_STATE_MINUS):
	GPIO.output(15, B)
    if (C!=C_STATE_MINUS):
	GPIO.output(16, C)

    # Set Past State
    A_STATE_MINUS = A
    B_STATE_MINUS = B
    C_STATE_MINUS = C

def board_select(C,B,A):
    # GPIO24 is Pin18
    # GPIO25 is Pin22
    # GPIO27 is Pin13
    #GPIO.setup(18, GPIO.OUT)
    #GPIO.setup(22, GPIO.OUT)
    #GPIO.setup(13, GPIO.OUT)
    global A_BOARD_SELECT_MINUS
    global B_BOARD_SELECT_MINUS
    global C_BOARD_SELECT_MINUS

    if (A!=A_BOARD_SELECT_MINUS):
	GPIO.output(18, A)
    if (B!=B_BOARD_SELECT_MINUS):
	GPIO.output(22, B)
    if (C!=C_BOARD_SELECT_MINUS):
	GPIO.output(13, C)

    # Set Past State
    A_BOARD_SELECT_MINUS = A
    B_BOARD_SELECT_MINUS = B
    C_BOARD_SELECT_MINUS = C

# Far left 2 lights
def load_relays(B,A):
    # GPIO4 is Pin7
    # GPIO17 is Pin11
    #GPIO.setup(7, GPIO.OUT)
    #GPIO.setup(11, GPIO.OUT)
    global A_RAS_MINUS
    global B_RAS_MINUS

    if (A!=A_RAS_MINUS):
	GPIO.output(7, A) 
    if (B!=B_RAS_MINUS):
	GPIO.output(11, B)

    # Set Past State
    A_RAS_MINUS = A
    B_RAS_MINUS = B

def invert_binary(state):
    ''' state = type is tuple, in binary '''
    B = str(state[0])
    A = str(state[1])
    result = []
    if B == '0':
	result.append(int(B.replace("0","1")))
    else:
	result.append(int(B.replace("1","0")))
    if A == '0':
        result.append(int(A.replace("0","1")))
    else:
        result.append(int(A.replace("1","0")))
    return result

def change_states(channel_addr,load_state,mux_state):
    ''' channel_addr = type is tuple, for board select
	load_state = type is tuple, for load_relays
	mux_state = type is tuple, for mux_relays	'''

    # Beause logic for load relays are inverted on board
    load_state = invert_binary(load_state)

    list_of_mux_state_addr =  {(0,0,0,0,1):(1,0,0),(0,0,0,1,0):(0,1,1),\
	(0,0,1,0,0):(0,1,0),(0,1,0,0,0):(0,0,1),(1,0,0,0,0):(0,0,0)}

    mux_state_addr = list_of_mux_state_addr[mux_state]

    board_select(channel_addr[0],channel_addr[1],channel_addr[2])
    load_relays(load_state[0],load_state[1])
    mux_relays(mux_state_addr[0],mux_state_addr[1],mux_state_addr[2])

def reset_all_gpio():
    GPIO.output(12, 0)
    GPIO.output(15, 0)
    GPIO.output(16, 0)
    GPIO.output(18, 0)
    GPIO.output(22, 0)
    GPIO.output(13, 0)
    GPIO.output(7, 0)
    GPIO.output(11, 0)
