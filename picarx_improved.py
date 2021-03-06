try:
    from ezblock import *
    from ezblock.__init__ import __reset_mcu__
    __reset_mcu__()
    time.sleep(0.01)
except ImportError:
    print ("This  computer  does  not  appear  to be a PiCar -X system(/opt/ezblock  is not  present). Shadowing  hardware  callswith  substitute  functions ")
    from  sim_ezblock  import *
import time
import logging
from logdecorator import log_on_start, log_on_end, log_on_error
import atexit
import math

logging_format = "%(asctime)s: %(message)s"
logging.basicConfig(format=logging_format, level=logging.INFO, datefmt ="%H:%M:%S")
logging.getLogger ().setLevel(logging.DEBUG)




PERIOD = 4095
PRESCALER = 10
TIMEOUT = 0.02

dir_servo_pin = Servo(PWM('P2'))
camera_servo_pin1 = Servo(PWM('P0'))
camera_servo_pin2 = Servo(PWM('P1'))
left_rear_pwm_pin = PWM("P13")
right_rear_pwm_pin = PWM("P12")
left_rear_dir_pin = Pin("D4")
right_rear_dir_pin = Pin("D5")

S0 = ADC('A0')
S1 = ADC('A1')
S2 = ADC('A2')

Servo_dir_flag = 1
dir_cal_value = 10
cam_cal_value_1 = 0
cam_cal_value_2 = 0
motor_direction_pins = [left_rear_dir_pin, right_rear_dir_pin]
motor_speed_pins = [left_rear_pwm_pin, right_rear_pwm_pin]
cali_dir_value = [1, -1]
cali_speed_value = [0, 0]

for pin in motor_speed_pins:
    pin.period(PERIOD)
    pin.prescaler(PRESCALER)

@log_on_start(logging.DEBUG , "set_motor_speed start")
@log_on_error(logging.DEBUG, "set_motor_speed error")
@log_on_end(logging.DEBUG, "set_motor_speed end")
def set_motor_speed(motor, speed):
    global cali_speed_value,cali_dir_value
    motor -= 1
    if speed >= 0:
        direction = 1 * cali_dir_value[motor]
    elif speed < 0:
        direction = -1 * cali_dir_value[motor]
    speed = abs(speed)
    # if speed != 0:
    #     speed = int(speed /2 ) + 50
    speed = speed - cali_speed_value[motor]
    if direction < 0:
        motor_direction_pins[motor].high()
        motor_speed_pins[motor].pulse_width_percent(speed)
    else:
        motor_direction_pins[motor].low()
        motor_speed_pins[motor].pulse_width_percent(speed)

@log_on_start(logging.DEBUG , "motor_speed_calibration start")
@log_on_error(logging.DEBUG, "motor_speed_calibration error")
@log_on_end(logging.DEBUG, "motor_speed_calibration end")
def motor_speed_calibration(value):
    global cali_speed_value,cali_dir_value
    cali_speed_value = value
    if value < 0:
        cali_speed_value[0] = 0
        cali_speed_value[1] = abs(cali_speed_value)
    else:
        cali_speed_value[0] = abs(cali_speed_value)
        cali_speed_value[1] = 0

@log_on_start(logging.DEBUG , "motor_direction_calibration start")
@log_on_error(logging.DEBUG, "motor_direction_calibration error")
@log_on_end(logging.DEBUG, "motor_direction_calibration end")
def motor_direction_calibration(motor, value):
    # 0: positive direction
    # 1:negative direction
    global cali_dir_value
    motor -= 1
    if value == 1:
        cali_dir_value[motor] = -1*cali_dir_value[motor]

@log_on_start(logging.DEBUG , "dir_servo_angle_calibration start")
@log_on_error(logging.DEBUG, "dir_servo_angle_calibration error")
@log_on_end(logging.DEBUG, "dir_servo_angle_calibration end")
def dir_servo_angle_calibration(value):
    global dir_cal_value
    dir_cal_value = value
    set_dir_servo_angle(dir_cal_value)
    # dir_servo_pin.angle(dir_cal_value)

@log_on_start(logging.DEBUG , "set_dir_servo_angle start")
@log_on_error(logging.DEBUG, "set_dir_servo_angle error")
@log_on_end(logging.DEBUG, "set_dir_servo_angle end")
def set_dir_servo_angle(value):
    global dir_cal_value
    dir_servo_pin.angle(value+dir_cal_value)

@log_on_start(logging.DEBUG , "camera_servo1_angle_calibration start")
@log_on_error(logging.DEBUG, "camera_servo1_angle_calibration error")
@log_on_end(logging.DEBUG, "camera_servo1_angle_calibration end")
def camera_servo1_angle_calibration(value):
    global cam_cal_value_1
    cam_cal_value_1 = value
    set_camera_servo1_angle(cam_cal_value_1)
    # camera_servo_pin1.angle(cam_cal_value)

@log_on_start(logging.DEBUG , "camera_servo2_angle_calibration start")
@log_on_error(logging.DEBUG, "camera_servo2_angle_calibration error")
@log_on_end(logging.DEBUG, "camera_servo2_angle_calibration end")
def camera_servo2_angle_calibration(value):
    global cam_cal_value_2
    cam_cal_value_2 = value
    set_camera_servo2_angle(cam_cal_value_2)
    # camera_servo_pin2.angle(cam_cal_value)

@log_on_start(logging.DEBUG , "set_camera_servo1_angle start")
@log_on_error(logging.DEBUG, "set_camera_servo1_angle error")
@log_on_end(logging.DEBUG, "set_camera_servo1_angle end")
def set_camera_servo1_angle(value):
    global cam_cal_value_1
    camera_servo_pin1.angle(-1 *(value+cam_cal_value_1))

@log_on_start(logging.DEBUG , "set_camera_servo2_angle start")
@log_on_error(logging.DEBUG, "set_camera_servo2_angle error")
@log_on_end(logging.DEBUG, "set_camera_servo2_angle end")
def set_camera_servo2_angle(value):
    global cam_cal_value_2
    camera_servo_pin2.angle(-1 * (value+cam_cal_value_2))

@log_on_start(logging.DEBUG , "get_adc_value start")
@log_on_error(logging.DEBUG, "get_adc_value error")
@log_on_end(logging.DEBUG, "get_adc_value end")
def get_adc_value():
    adc_value_list = []
    adc_value_list.append(S0.read())
    adc_value_list.append(S1.read())
    adc_value_list.append(S2.read())
    return adc_value_list

@log_on_start(logging.DEBUG , "set_power start")
@log_on_error(logging.DEBUG, "set_power error")
@log_on_end(logging.DEBUG, "set_power end")
def set_power(speed):
    set_motor_speed(1, speed)
    set_motor_speed(2, speed) 

@log_on_start(logging.DEBUG , "backward start")
@log_on_error(logging.DEBUG, "backward error")
@log_on_end(logging.DEBUG, "backward end")
def backward(speed):
    set_motor_speed(1, speed)
    set_motor_speed(2, speed)

@log_on_start(logging.DEBUG , "forward start")
@log_on_error(logging.DEBUG, "forward error")
@log_on_end(logging.DEBUG, "forward end")
def forward(speed, steering_angle):
    W = 3.5
    dr = 4.5
    s1 = speed
    s2 = s1 * ((W+dr*math.tan(math.radians(steering_angle))) / W)

    # print(steering_angle)
    # print(speed)
    # print(s1)
    # print(s2)

    set_motor_speed(1, -1*s1)
    set_motor_speed(2, -1*s2)

    # set_motor_speed(1, -1*speed)
    # set_motor_speed(2, -1*speed)

@log_on_start(logging.DEBUG , "stop start")
@log_on_error(logging.DEBUG, "stop error")
@log_on_end(logging.DEBUG, "stop end")
def stop():
    set_motor_speed(1, 0)
    set_motor_speed(2, 0)

@log_on_start(logging.DEBUG , "Get_distance start")
@log_on_error(logging.DEBUG, "Get_distance error")
@log_on_end(logging.DEBUG, "Get_distance end")
def Get_distance():
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
def test():
    # dir_servo_angle_calibration(-10) 
    set_dir_servo_angle(-40)
    # time.sleep(1)
    # set_dir_servo_angle(0)
    # time.sleep(1)
    # set_motor_speed(1, 1)
    # set_motor_speed(2, 1)
    # camera_servo_pin.angle(0)


# if __name__ == "__main__":
#     try:
#         # dir_servo_angle_calibration(-10) 
#         while 1:
#             test()
#     finally: 
#         stop()

# steering_angle = 20
# set_dir_servo_angle(steering_angle)
atexit.register(stop)



