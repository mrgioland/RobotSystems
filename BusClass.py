try:
    from ezblock import *
    from ezblock.__init__ import __reset_mcu__
    __reset_mcu__()
    time.sleep(0.01)
except ImportError:
    print("This  computer  does  not  appear  to be a PiCar -X system(/opt/ezblock  is not  present). Shadowing  hardware  callswith  substitute  functions ")
    from sim_ezblock import *

import numpy as np


class BusClass():

    def __init__(self):
        self.msg = []


    def bWrite(self, msg):
        self.msg = msg

    def bRead(self):
        return self.msg

    def test(self):
        print(self.bRead())
        self.bWrite('a')
        print(self.bRead())

        return 1


if __name__ == "__main__":
    tmp = BusClass()
    tmp.test()
    # print(tmp.sensor_reading())






