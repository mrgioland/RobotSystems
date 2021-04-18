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


def photocellSCI():
    interClass = InterpreterClass(1100)
    sensorc = sc.SenseClass()
    contr = cc.ControllerClass()

    pc.picarxClass().forward(10)

    while True:
        reading = sensorc.sensor_reading()
        pos = -1*interClass.getDirection(reading)
        contr.Control(pos)
        time.sleep(0.1)


def cameraSCI():
    a=1



if __name__ == "__main__":
    a=1
    photocellSCI()






