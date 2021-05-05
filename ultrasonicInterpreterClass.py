try:
    from ezblock import *
    from ezblock.__init__ import __reset_mcu__
    __reset_mcu__()
    time.sleep(0.01)
except ImportError:
    print("This  computer  does  not  appear  to be a PiCar -X system(/opt/ezblock  is not  present). Shadowing  hardware  callswith  substitute  functions ")
    from sim_ezblock  import *




 


class ultrasonicInterpreterClass():
    def __init__(self):
        self.dist = 1

    def getDirection(self, dist):
        if dist < 10:
            return 0
        else:
            return 1

    def test(self):
        return 1


if __name__ == "__main__":
    tmp = ultrasonicInterpreterClass()
    # print(tmp.getDirection(50))







