# main.py -- put your code here!
from pyb import Timer, UART, ADC, Pin, ExtInt
import pyb
import time

# Displays Error messages
import micropython
micropython.alloc_emergency_exception_buf(100)

# Virtual UART Port
ser = pyb.USB_VCP(0)

# Count steps moved
count = 0

# Track encoder phases
last_phase = 0
phase = 0

# How many steps to move the assay
ONE_STEP = 287
TWO_STEPS = 574

#Tracks the toggle state of the current device
servo_state1 = [0]
servo_state2 = [0]
servo_state3 = [0]
dc_state1 = [0]

Pins = {
        #Sci Assay
        0 : {
            #Top tray
            0 : {
                0 : "(Timer(8, freq=1250)).channel(1, Timer.PWM, pin=Pin('Y1'))",  #PWM Pin
                1 : Pin('Y2',Pin.OUT_PP),                                          #Dir Pin
                2 : Pin('Y3',Pin.OUT_PP),                                          #ENA Pin
                3: Pin('X7'),  # Encoder A
                4: Pin('Y12')  # Encoder B                                        
                },                                                
            #Bot tray
            1 : {
                0 : "(Timer(2, freq=1250)).channel(3, Timer.PWM, pin=Pin('Y9'))",  
                1 : Pin('X8',Pin.OUT_PP),  
                2 : Pin('Y10',Pin.OUT_PP),
                3: Pin('X6'),  # Encoder A
                4: Pin('Y11')  # Encoder B
                }             
            },
        #Soil Distrabution
        1 : {
            #Top Layer
            0 : {
                0 : pyb.Servo(1) #Servo 1 at X1
                },
            #Mid Layer
            1 : {
                0 : pyb.Servo(2)
                },
            #Bottom Layer
            2 : {
                0 : pyb.Servo(3)
                }
            },
        #Vibrator
        2 : {
            0 : {
                0 : Pin('X21',Pin.OUT_PP), #in1
                1 : Pin('X22',Pin.OUT_PP)  #in2
                }
            }
}

# Driver function for top encoder step_count
def top_count(line):
    global phase
    global last_phase
    global pin_t_A, pin_t_B
    last_phase = phase
    if pin_t_A.value() == 0:  # Might be able to use Pins[0][0][3].value()
        if pin_t_B.value() == 0:
            phase = 1
        else:
            phase = 2
    else:
        if pin_t_B.value() == 0:
            phase = 4
        else:
            phase = 3

    global count
    if (last_phase == 4) & (phase == 1):
        count += 1
    elif (last_phase == 1) & (phase == 4):
        count -= 1

# Driver function for bottom encoder step_count
def bot_count(line):
    global phase
    global last_phase
    global pin_b_A, pin_b_B
    last_phase = phase
    if pin_b_A.value() == 0:
        if pin_b_B.value() == 0:
            phase = 1
        else:
            phase = 2
    else:
        if pin_b_B.value() == 0:
            phase = 4
        else:
            phase = 3

    global count
    if (last_phase == 4) & (phase == 1):
        count += 1
    elif (last_phase == 1) & (phase == 4):
        count -= 1
        # print('phase: ' + str(phase))

# External Interrupt Pins and Object for the Top Motor Encoder
pin_t_A = Pins[0][0][3]
pin_t_B = Pins[0][0][4]
assay_enc_t_A = ExtInt(pin_t_A, ExtInt.IRQ_RISING_FALLING, Pin.PULL_UP, top_count)
assay_enc_t_B = ExtInt(pin_t_B, ExtInt.IRQ_RISING_FALLING, Pin.PULL_UP, top_count)


# External Interrupt Pins and Objects for the Bottom Motor Encoder
pin_b_A = Pins[0][0][3]
pin_b_B = Pins[0][0][4]
assay_enc_b_A = ExtInt(Pins[0][1][3], ExtInt.IRQ_RISING_FALLING, Pin.PULL_UP, bot_count)
assay_enc_b_B = ExtInt(Pins[0][1][4], ExtInt.IRQ_RISING_FALLING, Pin.PULL_UP, bot_count)

# Pulse an assay motor
def assayMove(stepper, dir_port, en_port, dir_val, count_val):
    # en_port.low()
    # stepper = (Timer(2, freq=1250)).channel(1, Timer.PWM, pin=Pin('Y9'))
    dir_port.value(dir_val)
    global count
    count = 0
    # print('Assay move count: '+str(count))
    stepper.pulse_width_percent(50)
    pyb.LED(4).on()
    while (count < count_val) & (count > -count_val):
        # print('Assay move count: '+str(count))
        pass
    stepper.pulse_width_percent(0)
    pyb.LED(4).off()
    # print('Assay move count: '+str(count))
    # en_port.high()

def toggleSoilPartition(servo, state):
    time.sleep(.4)
    if(state[0] == 0):
        servo.angle(45)
        state[0] = 1
    else:
        state[0] = 0
        servo.angle(-45)

def toggleVibrator(in1,in2,state):
    time.sleep(.4)
    if(state[0] == 0):
        in1.high()
        in2.low()
        state[0] = 1
    else:
        in1.low()
        in2.high()
        state[0] = 0

def stopVibrator(in1,in2):
    time.sleep(.4)
    in1.low()
    in2.low()

soilAction = {
        0 : {
            0 : {                   #PWM Port        #DIR Port     #ENA Port   #DIR  #Mode
                0 : 'assayMove(eval(Pins[0][0][0]), Pins[0][0][1], Pins[0][0][2], 1, ONE_STEP)',   #Top CW 1
                1 : 'assayMove(eval(Pins[0][0][0]), Pins[0][0][1], Pins[0][0][2], 0, ONE_STEP)',   #Top CCW 1
                2 : 'assayMove(eval(Pins[0][0][0]), Pins[0][0][1], Pins[0][0][2], 0, TWO_STEPS)'   #Top CCW 2
                },        
            1 : {
                0 : 'assayMove(eval(Pins[0][1][0]), Pins[0][1][1], Pins[0][1][2], 0, ONE_STEP)'    #Bot CCW 1
                } 
            },

        1 : {
            0 : {                          #Servo       #State
                0 : 'toggleSoilPartition(Pins[1][0][0],servo_state1)' #Toggle top
                },
            1 : {
                0 : 'toggleSoilPartition(Pins[1][1][0],servo_state2)' #Toggle mid
                },
            2 : {
                0 : 'toggleSoilPartition(Pins[1][2][0],servo_state3)' #Toggle bot
                }
            },

        2 : {
            0 : {                       #in1        #in2         #State
                0 : 'toggleVibrator(Pins[2][0][0],Pins[2][0][1],dc_state1)', #Toggle Vibrator 
                1 : 'stopVibrator(Pins[2][0][0],Pins[2][0][1])'              #Stop Vibrator
                }
            }
}

#TODO: Depending on the serial command given, wait for count to reach 1 or 2 assay movements
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
                    eval(soilAction[int(move[0])][int(move[1])][int(move[2])])
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
    #         eval(soilAction[0][0][0])
    #     elif(but_top_ccw.value()):
    #         eval(soilAction[0][0][1])
    #     elif(but_part_1.value()):
    #         eval(soilAction[1][0][0])

    # Setup all the ports and devices to default states
    eval(Pins[0][0][0])
    eval(Pins[0][1][0])
    Pins[0][0][2].low()
    Pins[0][1][2].low()

    Pins[1][0][0].angle(-180)
    Pins[1][1][0].angle(-180)
    Pins[1][2][0].angle(-180)

    stopVibrator(Pins[2][0][0],Pins[2][0][1])
    
    getCommand()
