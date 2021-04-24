try:
    from ezblock import *
    from ezblock.__init__ import __reset_mcu__
    __reset_mcu__()
    time.sleep(0.01)
except ImportError:
    print("This  computer  does  not  appear  to be a PiCar -X system(/opt/ezblock  is not  present). Shadowing  hardware  callswith  substitute  functions ")
    from sim_ezblock import *

import BusClass
import concurrent.futures
from threading import Lock
import time

from InterpreterClass import InterpreterClass
import ControllerClass as cc
import picarxClass as pc


def sensorProducerFunction(sensorBus):
    return sensorBus

def sensor_function(sensorBus, delay):
    lock = Lock()
    while True:
        tmpMsg = [0, 0, 0]
        with lock:
            tmpMsg[0] = sensorBus.S0.read()
            tmpMsg[1] = sensorBus.S1.read()
            tmpMsg[2] = sensorBus.S2.read()

        sensorBus.bWrite(tmpMsg)
        time.sleep(delay)


def interpretation_function(sensorBus, interpreterBus, delay):
    interClass = InterpreterClass(1100)

    while True:
        greyscale = sensorBus.bRead()
        if not(greyscale):
            time.sleep(delay)
            return
            continue

        #get position, write to bus msg field
        p = interClass.getDirection(greyscale)
        interpreterBus.bWrite(p)

        #delay
        time.sleep(delay)

def controller_function(interpreterBus, delay):
    contr = cc.ControllerClass()

    pc.picarxClass().forward(10)

    while True:
        pos = -1*interpreterBus.bRead()
        if not(pos):
            time.sleep(delay)
            continue
        contr.Control(pos)
        time.sleep(delay)


def ConsumerProducers(inBus, delay):
    while True:
        time.sleep(delay)

def Consumers(inBus):
    return inBus.bRead()

def test(inBus):
    a=1
    # print(Consumers(inBus))




if __name__ == "__main__":
    sensor_delay = 0.1
    interpreter_delay = 0.1
    controller_delay = 0.1
    sensor_value_bus = BusClass.BusClass()
    interpreter_bus = BusClass.BusClass()

    sensor_value_bus.S0 = ADC('A0')
    sensor_value_bus.S1 = ADC('A1')
    sensor_value_bus.S2 = ADC('A2')

    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        eSensor = executor.submit(sensor_function, sensor_value_bus, sensor_delay)
        eInterpreter = executor.submit(interpretation_function, sensor_value_bus, interpreter_bus, interpreter_delay)
        eController = executor.submit(controller_function, interpreter_bus, controller_delay)

    #
    # interpretation_function(sensor_value_bus, interpreter_bus, interpreter_delay)
    # controller_function(interpreter_bus,controller_delay)
    # a = sensor_function(sensor_value_bus, interpreter_bus,sensor_delay)
    # print(a.msg)
    # test(sensor_value_bus)


















