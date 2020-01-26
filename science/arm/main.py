from pyb import Pin, Timer, UART, ADC
import pyb
import time

#TODO: Add 1 DC motor and 1 limit switch

                           # Pwm      # Dir      # Enab (HIGH = Disable)
armAction = { 0 : { 0 : {4 : 'X1',  5 : 'X11',  6 : 'X12'},               # CH1 TIM2    Joint 1 ===> low = CLKW,    high = CCW,     freq = 1250  (Top)
                    1 : {4 : 'X2',  5 : 'X9',  6 : 'X10'},                # CH2 TIM2    Joint 2 ===> low = CLKW,    high = CCW,      freq = 1250  (Front)
                    2 : {4 : 'X3',  5 : 'X7',  6 : 'X8'},                 # CH3 TIM2    Joint 3 ===> low = CLKW,    high = CCW      freq = 1250  (Top)
                    3 : {4 : 'X4',  5 : 'X6',  6 : 'X5'}                  # CH4 TIM2    Joint 3 ===> low = CLKW,    high = CCW      freq = 1250  (Top)
                  },
                  #DC Motor Pinouts
              1 : { 0 : { 0 : Pin('Y5',Pin.OUT_PP), #in1
                          1 : Pin('Y6',Pin.OUT_PP)  #in2
                        }
                  },
              # Signal pin for limit switch
              2 : { 0 : {0 : Pin('X17', Pin.OUT)} }
            }
                            # Counter Clockwise / Left                  # Clockwise / Right                          # Stop                                       # Start
movements = { 0 : { 0 : {4 : Pin(armAction[0][5], Pin.OUT_PP).high, 5 : Pin(armAction[0][5], Pin.OUT_PP).low, 6 : Pin(armAction[0][6], Pin.OUT_PP).high, 7 : Pin(armAction[0][6], Pin.OUT_PP).low},
                            # UP                                         # Down                                      # Stop                                       # Start
                    1 : {4 : Pin(armAction[1][5], Pin.OUT_PP).high, 5 : Pin(armAction[1][5], Pin.OUT_PP).low, 6 : Pin(armAction[1][6], Pin.OUT_PP).high, 7 : Pin(armAction[1][6], Pin.OUT_PP).low},
                            # Counter Clockwise / Left                  # Clockwise / Right                          # Stop                                       # Start
                    2 : {4 : Pin(armAction[2][5], Pin.OUT_PP).high, 5 : Pin(armAction[2][5], Pin.OUT_PP).low, 6 : Pin(armAction[2][6], Pin.OUT_PP).high, 7 : Pin(armAction[2][6], Pin.OUT_PP).low}
                            # Counter Clockwise / Left                  # Clockwise / Right                          # Stop                                       # Start
                    2 : {4 : Pin(armAction[3][5], Pin.OUT_PP).high, 5 : Pin(armAction[3][5], Pin.OUT_PP).low, 6 : Pin(armAction[3][6], Pin.OUT_PP).high, 7 : Pin(armAction[3][6], Pin.OUT_PP).low}
                  },
                  #DC motor
              1 : { 0 : {0 : Pin(fluidicsPins[1][0][4], Pin.OUT).high(),  #ON
                         1 : Pin(fluidicsPins[1][0][4], Pin.OUT).low(),   #OFF
                         'cmd' : 0
                        }
                  }
            }

def getcommand():
    ser = UART(6, 115200)
    while True:
        try:
            data = ser.read(1)
            if str(data.decode('utf-8')) == 's':
                move = ser.read(3)
                move = move.decode('utf-8')
                if str(move[2]) == 'e':
                    pyb.LED(3).toggle();
                    movements[int(move[0])][int(move[1])]()
                    pyb.LED(3).toggle();
        except:
            pass

if __name__ == "__main__":
    for i in range(4): #movements, armAction, and ledMove are arrays, an array of 4, will be 5 since a 5th motor to be added
    #armAction setting up the pins on the board to specify what is the en, dir, and pulse_width_percent
    #movments detailing what way to move or Stop
    #ledMove lights on the board light up to signal what and how things are moving
        Pin(armAction[i][6], Pin.OUT_PP).high()
        Pin(armAction[i][5], Pin.OUT_PP).high()
        Timer(2, freq=1250).channel(i+1, Timer.PWM, pin=Pin(armAction[i][4])).pulse_width_percent(50)
    #initialize DC pins
    Pin(armAction[1][0][0], Pin.OUT).low()
    Pin(armAction[1][0][1], Pin.OUT).low()
    pyb.LED(2).toggle()
    time.sleep(1)
    pyb.LED(2).toggle()
    getcommand()
