
try:
    from ezblock import *
    from ezblock.__init__ import __reset_mcu__
    __reset_mcu__()
    time.sleep(0.01)
except ImportError:
    print("This  computer  does  not  appear  to be a PiCar -X system(/opt/ezblock  is not  present). Shadowing  hardware  callswith  substitute  functions ")
    from  sim_ezblock  import *
# from picarxClass import *
import picarxClass as pc
import time
import atexit
from logdecorator import log_on_start, log_on_end, log_on_error
import math

# logging_format = "%(asctime)s: %(message)s"
# logging.basicConfig(format=logging_format, level=logging.INFO, datefmt ="%H:%M:%S")
# logging.getLogger ().setLevel(logging.DEBUG)


class ControllerClass():

    def __init__(self, scaling=1):
        #light = 0, dark = 1
        self.scaling = scaling

    def Control(self, modifier):
        ang = 20 * modifier
        pc.picarxClass().set_dir_servo_angle(ang)
        return ang




if __name__ == "__main__":
    tmp = ControllerClass()
    # tmp.Control(5)









