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

logging_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=logging_format, level=logging.INFO, datefmt ="%H:%M:%S")
logging.getLogger ().setLevel(logging.DEBUG)


class SenseClass():

    def __init__(self):
        self.S0 = ADC('A0')
        self.S1 = ADC('A1')
        self.S2 = ADC('A2')

    def sensor_reading(self):
         return [self.S0.read(), self.S1.read(), self.S2.read()]



    def test(self):


        return 1


if __name__ == "__main__":
    tmp = SenseClass()
    print(tmp.sensor_reading())







