# main.py -- put your code here!
from pyb import Pin, Timer, UART, ADC, USB_VCP
import pyb
import time
import _thread


                   # Pwm      # Dir      # Enab (HIGH = Disable)
armAction = { 0 : {4 : 'X1',  5 : 'X5',  6 : 'X6'},               # CH1 TIM2    Joint 1 ===> low = CLKW,    high = CCW,     freq = 1250  (Top)
              1 : {4 : 'X2',  5 : 'X7',  6 : 'X8'},               # CH2 TIM2    Joint 2 ===> low = DOWN,    high = UP,      freq = 1250  (Front)
              2 : {4 : 'X3',  5 : 'X9',  6 : 'X10'},              # CH3 TIM2    Joint 3 ===> low = CLKW,    high = CCW      freq = 1250  (Top)
              3 : {4 : 'X4',  5 : 'X11', 6 : 'X12'},              # CH4 TIM2    Joint 4 ===> low = OPEN/CLOSE, high = OPEN/CLOSE    freq = 1250  (Front)
              4 : {4 : 'Y2',  5 : 'X19', 6 : 'X20'}               # FILL IN
            }

                       # Counter Clockwise / Left                 # Clockwise / Right                       # Stop                                     # Start 
movements = { 0 : {4 : Pin(armAction[0][5], Pin.OUT_PP).high, 5 : Pin(armAction[0][5], Pin.OUT_PP).low, 6 : Pin(armAction[0][6], Pin.OUT_PP).high, 7 : Pin(armAction[0][6], Pin.OUT_PP).low},
                       # UP                                       # Down                                    # Stop                                     # Start 
              1 : {4 : Pin(armAction[1][5], Pin.OUT_PP).high, 5 : Pin(armAction[1][5], Pin.OUT_PP).low, 6 : Pin(armAction[1][6], Pin.OUT_PP).high, 7 : Pin(armAction[1][6], Pin.OUT_PP).low},
                       # Counter Clockwise / Left                 # Clockwise / Right                       # Stop                                     # Start 
              2 : {4 : Pin(armAction[2][5], Pin.OUT_PP).high, 5 : Pin(armAction[2][5], Pin.OUT_PP).low, 6 : Pin(armAction[2][6], Pin.OUT_PP).high, 7 : Pin(armAction[2][6], Pin.OUT_PP).low},
                       # Close / Open                             # Close / Open                            # Stop                                     # Start 
              3 : {4 : Pin(armAction[3][5], Pin.OUT_PP).high, 5 : Pin(armAction[3][5], Pin.OUT_PP).low, 6 : Pin(armAction[3][6], Pin.OUT_PP).high, 7 : Pin(armAction[3][6], Pin.OUT_PP).low},
                       # FILL IN
              4 : {4 : Pin(armAction[4][5], Pin.OUT_PP).high, 5 : Pin(armAction[4][5], Pin.OUT_PP).low, 6 : Pin(armAction[4][6], Pin.OUT_PP).high, 7 : Pin(armAction[4][6], Pin.OUT_PP).low}
            }

#  SAMPLE COMMAND READ 8##9
def getcommand():
    #ser = UART(6, 115200)
    ser = USB_VCP() # Micro USB port to host
    while True:
        try:
            data = ser.read(1)
            if str(data.decode('utf-8')) == 's':
                move = ser.read(3)
                move = move.decode('utf-8')
                if str(move[2]) == 'e':
                    movements[int(move[0])][int(move[1])]()
        except:
            pass

if __name__ == "__main__":
    for i in range(5):
        Pin(armAction[i][6], Pin.OUT_PP).high()
        Pin(armAction[i][5], Pin.OUT_PP).high()
        Timer(2, freq=1250).channel(i+1, Timer.PWM, pin=Pin(armAction[i][4])).pulse_width_percent(50)
    pyb.LED(2).toggle()
    time.sleep(1)
    pyb.LED(2).toggle()
    getcommand()
