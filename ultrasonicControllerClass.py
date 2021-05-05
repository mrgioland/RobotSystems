try:
    from ezblock import *
    from ezblock.__init__ import __reset_mcu__
    __reset_mcu__()
    time.sleep(0.01)
except ImportError:
    print("This  computer  does  not  appear  to be a PiCar -X system(/opt/ezblock  is not  present). Shadowing  hardware  callswith  substitute  functions ")
    from sim_ezblock  import *
import picarxClass as pc




 


class ultrasonicControllerClass():
    def __init__(self):
        self.a=1

    def Control(self, dir):
        if dir > 0:
            pc.picarxClass().stop()
        else:
            pc.picarxClass().forward(10)
        return dir


    def test(self):
        return 1


if __name__ == "__main__":
    tmp = ultrasonicControllerClass()
    # tmp.Control(0)
    # print(tmp.getDirection(50))







