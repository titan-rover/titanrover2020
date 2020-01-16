# main.py -- put your code here!
from pyb import Timer, UART, ADC, Pin, ExtInt
import pyb
import time

# Virtual UART Port
ser = pyb.USB_VCP(0)

#Tracks the toggle state of the current device
dc_state1 = [0]
dc_state2 = [0]
dc_state3 = [0]
dc_state4 = [0]
sol_state = [0]

Pins = {
        #Manafold
        0 : {
            0 : {
                0 : "(Timer(2, freq=1250)).channel(3, Timer.PWM, pin=Pin('X3'))",  #PWM Pin
                1 : Pin('X9',Pin.OUT_PP),                                          #Dir Pin
                2 : Pin('X10',Pin.OUT_PP)                                          #ENA Pin
                }
            },
        #Spectroscopy
        1 : {
            0 : {
                0 : "(Timer(2, freq=1250)).channel(4, Timer.PWM, pin=Pin('X4'))",  
                1 : Pin('X11',Pin.OUT_PP),  
                2 : Pin('Y12',Pin.OUT_PP)
                }
            },             
        #Pumps
        2 : {
            0 : {
                0 : Pin('Y1',Pin.OUT_PP), #in1
                1 : Pin('Y2',Pin.OUT_PP)  #in2
                },
            1 : {
                0 : Pin('Y3',Pin.OUT_PP), #in1
                1 : Pin('Y4',Pin.OUT_PP)  #in2
                },
            2 : {
                0 : Pin('Y5',Pin.OUT_PP), #in1
                1 : Pin('Y6',Pin.OUT_PP)  #in2
                },
            3 : {
                0 : Pin('Y7',Pin.OUT_PP), #in1
                1 : Pin('Y8',Pin.OUT_PP)  #in2
                }
            },
        #Solenoid
        3 : {
            0 : {
                0 : Pin('Y9',Pin.OUT_PP) #sig pin
                }
            }
}

# Pulse a stepper motor
def stepperMove(stepper, dir_port, en_port, dir_val):
    dir_port.value(dir_val)
    stepper.pulse_width_percent(50)
    pyb.LED(4).on()
    stepper.pulse_width_percent(0)
    pyb.LED(4).off()

def togglePump(in1,in2,state):
    time.sleep(.4)
    if(state[0] == 0):
        in1.high()
        in2.low()
        state[0] = 1
    else:
        in1.low()
        in2.high()
        state[0] = 0

def stopPump(in1,in2):
    time.sleep(.4)
    in1.low()
    in2.low()

def toggleSolenoid(sig,state):
    time.sleep(.4)
    if(state[0] == 0):
        sig.high()
        state[0] = 1
    else:
        sig.low()
        state[0] = 0

fluidAction = {
        0 : {
            0 : {                     #PWM Port         #DIR Port       #ENA Port  #DIR  
                0 : 'stepperMove(eval(Pins[0][0][0]), Pins[0][0][1], Pins[0][0][2], 1)',   #Manaf CW
                1 : 'stepperMove(eval(Pins[0][0][0]), Pins[0][0][1], Pins[0][0][2], 0)'    #Manaf CCW
                }
            },

        1 : {
            0 : {
                0 : 'stepperMove(eval(Pins[1][0][0]), Pins[1][0][1], Pins[1][0][2], 1)',   #Spect CW
                1 : 'stepperMove(eval(Pins[1][0][0]), Pins[1][0][1], Pins[1][0][2], 0)'    #Spect CCW
                } 
            },

        2 : {
            0 : {                       #in1        #in2       #State
                0 : 'togglePump(Pins[2][0][0],Pins[2][0][1],dc_state1)', #Toggle pump1 
                1 : 'stopPump(Pins[2][0][0],Pins[2][0][1])'              #Stop pum1
                },
            1 : {                       #in1        #in2       #State
                0 : 'togglePump(Pins[2][1][0],Pins[2][1][1],dc_state2)', #Toggle pump2 
                1 : 'stopPump(Pins[2][1][0],Pins[2][1][1])'              #Stop pump2
                },
            2 : {                       #in1        #in2       #State
                0 : 'togglePump(Pins[2][2][0],Pins[2][2][1],dc_state3)', #Toggle pump3 
                1 : 'stopPump(Pins[2][2][0],Pins[2][2][1])'              #Stop pump3
                },
            3 : {                       #in1        #in2       #State
                0 : 'togglePump(Pins[2][3][0],Pins[2][3][1],dc_state4)', #Toggle pump4 
                1 : 'stopPump(Pins[2][3][0],Pins[2][3][1])'              #Stop pump4
                }
            },
            
        3 : {
            0 : {                       #Sig pin   #State
                0 : 'toggleSolenoid(Pins[3][0][0],sol_state)'   #Toggle Solenoid 
                }
            }
            
}

def getCommand():
    while True:
        try:
            data = ser.read(1)
            time.sleep(.1)
            if str(data.decode('utf-8')) == 's':
                move = ser.read(4)
                move = move.decode('utf-8')
                if str(move[3]) == 'e':
                    time.sleep(1)
                    eval(fluidAction[int(move[0])][int(move[1])][int(move[2])])
        except:
            pass


if __name__ == "__main__":
    #Testing buttons
    # but_top_cw = Pin('Y6', Pin.IN, Pin.PULL_NONE)
    # but_top_ccw = Pin('Y7', Pin.IN, Pin.PULL_NONE)
    # but_bot_ccw = Pin('Y8', Pin.IN, Pin.PULL_NONE)
    # but_part_1 = Pin('X9', Pin.IN, Pin.PULL_NONE)
    # but_part_2 = Pin('X10', Pin.IN, Pin.PULL_NONE)
    # but_part_3 = Pin('X11', Pin.IN, Pin.PULL_NONE)
    # but_vibrator = Pin('X12', Pin.IN, Pin.PULL_NONE)

    # while True:
    #     if(but_top_cw.value()):
    #         eval(fluidAction[0][0][0])
    #     elif(but_top_ccw.value()):
    #         eval(fluidAction[0][0][1])
    #     elif(but_part_1.value()):
    #         eval(fluidAction[1][0])

   # Setup all the ports and devices to default states
    eval(Pins[0][0][0])
    eval(Pins[1][0][0])
    Pins[0][0][2].low()
    Pins[1][0][2].low()

    stopPump(Pins[2][0][0],Pins[2][0][1])
    stopPump(Pins[2][1][0],Pins[2][1][1])
    stopPump(Pins[2][2][0],Pins[2][2][1])
    stopPump(Pins[2][3][0],Pins[2][3][1])

    
    getCommand()
