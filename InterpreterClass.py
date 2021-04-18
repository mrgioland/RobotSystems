try:
    from ezblock import *
    from ezblock.__init__ import __reset_mcu__
    __reset_mcu__()
    time.sleep(0.01)
except ImportError:
    print("This  computer  does  not  appear  to be a PiCar -X system(/opt/ezblock  is not  present). Shadowing  hardware  callswith  substitute  functions ")
    from  sim_ezblock  import *
import time
import atexit
from logdecorator import log_on_start, log_on_end, log_on_error
import math
import sys
import logging

logging_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=logging_format, level=logging.INFO, datefmt ="%H:%M:%S")
logging.getLogger ().setLevel(logging.DEBUG)

class InterpreterClass():
    def __init__(self,sensitivity=1100, polarity=1):
        #light = 0, dark = 1
        self.sensitivity = sensitivity
        self.polarity = polarity

    def getDirection(self, greyscale):
        #default to polarity=1, light

        if (greyscale[0]) <= self.sensitivity:
            Left = 1
        else:
            Left = 0
        if (greyscale[1]) <= self.sensitivity:
            Mid = 1
        else:
            Mid = 0
        if (greyscale[2]) <= self.sensitivity:
            Right = 1
        else:
            Right = 0
        value = [Left, Mid, Right]

        #To set polarity to be dark, invert values
        if not self.polarity:
            print("SOMETHING IS WRONG")
            print("SOMETHING IS WRONG")
            print("SOMETHING IS WRONG")
            print("SOMETHING IS WRONG")
            print("SOMETHING IS WRONG")
            print("SOMETHING IS WRONG")
            print("SOMETHING IS WRONG")
            print("SOMETHING IS WRONG")
            value = [abs(x - 1) for x in value]

        #Determine direction to turn
        #1 = left, 0 = forward, -1 = right
        if value == [0, 1, 0] or value == [1, 1, 1]:
            direction = 'FORWARD'
            pos = 0
        elif value == [1, 0, 0]:
            direction = 'HARD LEFT'
            pos = 1
        elif value == [1, 1, 0]:
            direction = 'LEFT'
            pos = 0.5
        elif value == [0, 0, 1]:
            direction = 'HARD RIGHT'
            pos = -1
        elif value == [0, 1, 1]:
            direction = 'RIGHT'
            pos = -0.5
        elif value == [0, 0, 0]:
            direction = 'OUT'
            pos = 1.1

        print(greyscale)
        print(value)
        return pos

    def test(self):


        return 1


if __name__ == "__main__":
    tmp = InterpreterClass()
    # print(tmp.sensitivity)
    # print(tmp.edgeDection([1,0,0]))










