try:
    from ezblock import *
    from ezblock.__init__ import __reset_mcu__
    __reset_mcu__()
    time.sleep(0.01)
except ImportError:
    print("This  computer  does  not  appear  to be a PiCar -X system(/opt/ezblock  is not  present). Shadowing  hardware  callswith  substitute  functions ")
    from  sim_ezblock  import *
import sys
import SenseClass as sc
import ControllerClass as cc
from InterpreterClass import InterpreterClass
import picarxClass as pc
from rossros import *
import ultrasonicControllerClass as ucc
from ultrasonicInterpreterClass import ultrasonicInterpreterClass
import ultrasonicSenseClass as usc

def test_sensor_function(sensorBus, delay):
    while True:
        # tmpMsg = [0, 0, 0]
        # tmpMsg[0] = sc.SenseClass.S0()
        # tmpMsg[1] = sc.SenseClass.S1()
        # tmpMsg[2] = sc.SenseClass.S2()
        s = sc.SenseClass()
        tmpMsg = s.sensor_reading()
        sensorBus.set_message(tmpMsg, 'sensor')
        time.sleep(delay)

def sensor_function(sensorBus, delay):
    while True:
        # tmpMsg = [0, 0, 0]
        # tmpMsg[0] = sc.SenseClass.S0()
        # tmpMsg[1] = sc.SenseClass.S1()
        # tmpMsg[2] = sc.SenseClass.S2()
        s = sc.SenseClass()
        tmpMsg = s.sensor_reading()
        sensorBus.set_message(tmpMsg, 'sensor')
        time.sleep(delay)


def interpretation_function(sensorBus, interpreterBus, delay):
    interClass = InterpreterClass(1100)

    while True:
        greyscale = sensorBus.get_message('sensor')
        if not(greyscale):
            time.sleep(delay)
            return
            continue

        #get position, write to bus msg field
        p = interClass.getDirection(greyscale)
        interpreterBus.set_message(p, 'dir')

        #delay
        time.sleep(delay)


def controller_function(interpreterBus, delay):
    contr = cc.ControllerClass()

    pc.picarxClass().forward(10)

    while True:
        pos = -1*interpreterBus.get_message('dir')
        if not(pos):
            time.sleep(delay)
            continue
        contr.Control(pos)
        time.sleep(delay)




def ultrasensor_function(sensorBus, delay):
    while True:
        # tmpMsg = [0, 0, 0]
        # tmpMsg[0] = sc.SenseClass.S0()
        # tmpMsg[1] = sc.SenseClass.S1()
        # tmpMsg[2] = sc.SenseClass.S2()
        s = usc.ultrasonicSenseClass()
        tmpMsg = s.sensor_reading()
        sensorBus.set_message(tmpMsg, 'ultrasensor')
        time.sleep(delay)


def ultra_interpretation_function(sensorBus, interpreterBus, delay):
    interClass = ultrasonicInterpreterClass()

    while True:
        d = sensorBus.get_message('ultrasensor')

        #get position, write to bus msg field
        p = interClass.getDirection(d)
        interpreterBus.set_message(p, 'stopgo')

        #delay
        time.sleep(delay)


def ultra_controller_function(interpreterBus, delay):
    contr = ucc.ultrasonicControllerClass()

    # pc.picarxClass().forward(10)

    while True:
        toGo = interpreterBus.get_message('dir')
        contr.Control(toGo)
        time.sleep(delay)


def test():
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
        eSensor = executor.submit(sensor_function, sensor_value_bus, sensor_delay)
        eInterpreter = executor.submit(interpretation_function, sensor_value_bus, interpreter_bus, interpreter_delay)
        eController = executor.submit(controller_function, interpreter_bus, controller_delay)






if __name__ == "__main__":
    a=1
    default_termination_bus = Bus(False)
    default_input_bus = Bus()
    default_output_bus = Bus()

    sensor_value_bus = Bus()
    sensorObj = sc.SenseClass()

    direction_bus = Bus()
    # sensor_value_bus = Bus()








    #Line Follower
    # rosSensor1 = Producer('sensor_function', sensor_value_bus, 0.1, default_termination_bus, 'rosSensor1')
    rosSensor1 = Producer('sensor_function', sensor_value_bus, 0.1, default_termination_bus, 'rosSensor1')
    rosInterpreter1 = ConsumerProducer('interpretation_function', sensor_value_bus, direction_bus, 0.1, default_termination_bus, 'rosInterpreter1')
    rosController1 = Consumer('controller_function', direction_bus, 0.1, default_termination_bus, 'rosController1')


    #Ultrasonic stop/go
    ultrasonic_value_bus = Bus()
    stopgo_bus = Bus()
    rosSensor2 = Producer('ultrasensor_function', ultrasonic_value_bus, 0.1, default_termination_bus, 'rosSensor2')
    rosInterpreter2 = ConsumerProducer('ultra_interpretation_function', ultrasonic_value_bus, stopgo_bus, 0.1, default_termination_bus, 'rosInterpreter2')
    rosController2 = Consumer('ultra_controller_function', stopgo_bus, 0.1, default_termination_bus, 'rosController2')

    # sys.exit()
    #run
    runConcurrently([rosSensor1, rosController1, rosInterpreter1, rosSensor1, rosController1, rosInterpreter1])
    # runConcurrently([rosSensor1])



    # sys.exit()
    #
    # #Line Follower
    # rosSensor1 = Producer
    # # output sensorBus
    # # rosSensor1.__init__(sensor_function(sensor_value_bus, 0.1), sensor_value_bus)
    #
    # rosInterpreter1 = ConsumerProducer
    # # rosInterpreter1.__init__(interpretation_function(sensor_value_bus, direction_bus, 0.1), sensor_value_bus, direction_bus)
    # #input sensorBus
    # #output directionBus
    #
    # rosController1 = Consumer
    # #input directionBus
    # # rosController1.__init__(controller_function(direction_bus, 0.1), direction_bus)
    #
    #
    # #Ultrasonic stop/go
    # ultrasonic_value_bus = Bus()
    # stopgo_bus = Bus()
    #
    # rosSensor2 = Producer
    # # output sensorBus
    # # rosSensor2.__init__(ultrasensor_function(ultrasonic_value_bus, 0.1), ultrasonic_value_bus)
    #
    # rosInterpreter2 = ConsumerProducer
    # # rosInterpreter2.__init__(ultra_interpretation_function(ultrasonic_value_bus, stopgo_bus, 0.1), ultrasonic_value_bus, stopgo_bus)
    # #input sensorBus
    # #output directionBus
    #
    # rosController2 = Consumer
    # #input directionBus
    # # rosController2.__init__(ultra_controller_function(stopgo_bus, 0.1), stopgo_bus)
    #
    #
    # #run
    # runConcurrently([rosSensor1, rosController1, rosInterpreter1, rosSensor1, rosController1, rosInterpreter1])



