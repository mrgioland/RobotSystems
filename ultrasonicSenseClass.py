try:
    from ezblock import *
    from ezblock.__init__ import __reset_mcu__
    __reset_mcu__()
    time.sleep(0.01)
except ImportError:
    print("This  computer  does  not  appear  to be a PiCar -X system(/opt/ezblock  is not  present). Shadowing  hardware  callswith  substitute  functions ")
    from sim_ezblock import *
# from ezblock import Ultrasonic


class ultrasonicSenseClass():

    def __init__(self):
        self.pin_D0 = Pin("D0")
        self.pin_D1 = Pin("D1")

    def sensor_reading(self):
        return Ultrasonic(self.pin_D0, self.pin_D1).read()

    def test(self):
        return 1


if __name__ == "__main__":
    tmp = ultrasonicSenseClass()
    print(tmp.sensor_reading())








