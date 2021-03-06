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
import logging

logging_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=logging_format, level=logging.INFO, datefmt ="%H:%M:%S")
logging.getLogger ().setLevel(logging.DEBUG)

class picarxClass():

    def __init__(self):
        PERIOD = 4095
        PRESCALER = 10
        TIMEOUT = 0.02

        self.dir_servo_pin = Servo(PWM('P2'))
        self.camera_servo_pin1 = Servo(PWM('P0'))
        self.camera_servo_pin2 = Servo(PWM('P1'))
        self.left_rear_pwm_pin = PWM("P13")
        self.right_rear_pwm_pin = PWM("P12")
        self.left_rear_dir_pin = Pin("D4")
        self.right_rear_dir_pin = Pin("D5")

        self.S0 = ADC('A0')
        self.S1 = ADC('A1')
        self.S2 = ADC('A2')

        self.Servo_dir_flag = 1
        self.dir_cal_value = 10
        self.cam_cal_value_1 = 0
        self.cam_cal_value_2 = 0
        self.motor_direction_pins = [self.left_rear_dir_pin, self.right_rear_dir_pin]
        self.motor_speed_pins = [self.left_rear_pwm_pin, self.right_rear_pwm_pin]
        self.cali_dir_value = [1, -1]
        self.cali_speed_value = [0, 0]

        atexit.register(self.cleanup)

        for pin in self.motor_speed_pins:
            pin.period(PERIOD)
            pin.prescaler(PRESCALER)

    @log_on_start(logging.DEBUG, "cleanup start")
    @log_on_error(logging.DEBUG, "cleanup error")
    @log_on_end(logging.DEBUG, "cleanup end")
    def cleanup(self):
        self.set_dir_servo_angle(0)
        self.set_motor_speed(1,0)
        self.set_motor_speed(2,0)

    @log_on_start(logging.DEBUG, "set_motor_speed start")
    @log_on_error(logging.DEBUG, "set_motor_speed error")
    @log_on_end(logging.DEBUG, "set_motor_speed end")
    def set_motor_speed(self, motor, speed):
        motor -= 1
        if speed >= 0:
            direction = 1 * self.cali_dir_value[motor]
        elif speed < 0:
            direction = -1 * self.cali_dir_value[motor]
        speed = abs(speed)
        if speed != 0:
            speed = int(speed /2) + 50
        speed = speed - self.cali_speed_value[motor]
        if direction < 0:
            self.motor_direction_pins[motor].high()
            self.motor_speed_pins[motor].pulse_width_percent(speed)
        else:
            self.motor_direction_pins[motor].low()
            self.motor_speed_pins[motor].pulse_width_percent(speed)

    @log_on_start(logging.DEBUG, "motor_speed_calibration start")
    @log_on_error(logging.DEBUG, "motor_speed_calibration error")
    @log_on_end(logging.DEBUG, "motor_speed_calibration end")
    def motor_speed_calibration(self, value):
        self.cali_speed_value = value
        if value < 0:
            self.cali_speed_value[0] = 0
            self.cali_speed_value[1] = abs(self.cali_speed_value)
        else:
            self.cali_speed_value[0] = abs(self.cali_speed_value)
            self.cali_speed_value[1] = 0

    @log_on_start(logging.DEBUG, "motor_direction_calibration start")
    @log_on_error(logging.DEBUG, "motor_direction_calibration error")
    @log_on_end(logging.DEBUG, "motor_direction_calibration end")
    def motor_direction_calibration(self, motor, value):
        # 0: positive direction
        # 1:negative direction
        motor -= 1
        if value == 1:
            self.cali_dir_value[motor] = -1*self.cali_dir_value[motor]

    @log_on_start(logging.DEBUG, "dir_servo_angle_calibration start")
    @log_on_error(logging.DEBUG, "dir_servo_angle_calibration error")
    @log_on_end(logging.DEBUG, "dir_servo_angle_calibration end")
    def dir_servo_angle_calibration(self, value):
        self.dir_cal_value = value
        self.set_dir_servo_angle(self.dir_cal_value)

    @log_on_start(logging.DEBUG, "set_dir_servo_angle start")
    @log_on_error(logging.DEBUG, "set_dir_servo_angle error")
    @log_on_end(logging.DEBUG, "set_dir_servo_angle end")
    def set_dir_servo_angle(self, value):
        self.dir_servo_pin.angle(value+self.dir_cal_value)

    @log_on_start(logging.DEBUG, "get_adc_value start")
    @log_on_error(logging.DEBUG, "get_adc_value error")
    @log_on_end(logging.DEBUG, "get_adc_value end")
    def get_adc_value(self):
        adc_value_list = []
        adc_value_list.append(self.S0.read())
        adc_value_list.append(self.S1.read())
        adc_value_list.append(self.S2.read())
        return adc_value_list

    @log_on_start(logging.DEBUG, "set_power start")
    @log_on_error(logging.DEBUG, "set_power error")
    @log_on_end(logging.DEBUG, "set_power end")
    def set_power(self, speed):
        self.set_motor_speed(1, speed)
        self.set_motor_speed(2, speed)

    @log_on_start(logging.DEBUG, "backward start")
    @log_on_error(logging.DEBUG, "backward error")
    @log_on_end(logging.DEBUG, "backward end")
    def backward(self, speed):
        self.set_motor_speed(1, speed)
        self.set_motor_speed(2, speed)

    @log_on_start(logging.DEBUG, "forward start")
    @log_on_error(logging.DEBUG, "forward error")
    @log_on_end(logging.DEBUG, "forward end")
    def forward(self, speed):
        self.set_motor_speed(1, -1*speed)
        self.set_motor_speed(2, -1*speed)

    @log_on_start(logging.DEBUG, "stop start")
    @log_on_error(logging.DEBUG, "stop error")
    @log_on_end(logging.DEBUG, "stop end")
    def stop(self):
        self.set_motor_speed(1, 0)
        self.set_motor_speed(2, 0)

    @log_on_start(logging.DEBUG, "Get_distance start")
    @log_on_error(logging.DEBUG, "Get_distance error")
    @log_on_end(logging.DEBUG, "Get_distance end")
    def Get_distance(self):
        timeout=0.01
        trig = Pin('D8')
        echo = Pin('D9')

        trig.low()
        time.sleep(0.01)
        trig.high()
        time.sleep(0.000015)
        trig.low()
        pulse_end = 0
        pulse_start = 0
        timeout_start = time.time()
        while echo.value()==0:
            pulse_start = time.time()
            if pulse_start - timeout_start > timeout:
                return -1
        while echo.value()==1:
            pulse_end = time.time()
            if pulse_end - timeout_start > timeout:
                return -2
        during = pulse_end - pulse_start
        cm = round(during * 340 / 2 * 100, 2)
        #print(cm)
        return cm

    @log_on_start(logging.DEBUG, "test start")
    @log_on_error(logging.DEBUG, "test error")
    @log_on_end(logging.DEBUG, "test end")
    def test(self):
        # dir_servo_angle_calibration(-10)
        self.set_dir_servo_angle(-40)
        time.sleep(.1)
        self.set_dir_servo_angle(0)
        time.sleep(.1)
        self.set_motor_speed(1, 1)
        self.set_motor_speed(2, 1)
        self.forward(30)
        time.sleep(.1)
        self.backward(30)
        self.stop()


if __name__ == "__main__":
    tmp = picarxClass()
    print('a')
    tmp.test()

#     try:
#         # dir_servo_angle_calibration(-10)
#         while 1:
#             test()
#     finally:
#         stop()
