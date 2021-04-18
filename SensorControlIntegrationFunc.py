try:
    from ezblock import *
    from ezblock.__init__ import __reset_mcu__
    __reset_mcu__()
    time.sleep(0.01)
except ImportError:
    print("This  computer  does  not  appear  to be a PiCar -X system(/opt/ezblock  is not  present). Shadowing  hardware  callswith  substitute  functions ")
    from  sim_ezblock  import *
import SenseClass as sc
import ControllerClass as cc
from InterpreterClass import InterpreterClass
import picarxClass as pc


def SCI():
    interClass = InterpreterClass(1100)
    pc.picarxClass().forward(10)

    while True:
        reading = sc.SenseClass().sensor_reading()
        pos = -1*interClass.getDirection(reading)
        ang = cc.ControllerClass().Control(pos)

    return 1


if __name__ == "__main__":
    a=1
    SCI()






