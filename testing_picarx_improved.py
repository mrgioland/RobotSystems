from picarx_improved import *
import time
# dir_servo_angle_calibration(-10)
# set_dir_servo_angle(-40)
# time.sleep(1)
# set_dir_servo_angle(0)
# time.sleep(1)
# set_motor_speed(1, 1)
# set_motor_speed(2, 1)
# camera_servo_pin.angle(0)

# print("starting")
# set_dir_servo_angle(0)
# forward(50,0)
# time.sleep(2)
# print("done")
# stop()

def FwdBack():
    print("Starting Forward/Back")
    set_dir_servo_angle(0)
    forward(50,0)
    time.sleep(1)
    backward(50)
    print("done Forward/Back")
    print()


def ParallelParkingLeft():
    print("Starting Parallel Parking - Left")
    #turn
    set_dir_servo_angle(-40)
    backward(30)
    time.sleep(0.25)
    stop()
    #backup
    set_dir_servo_angle(0)
    backward(30)
    time.sleep(0.5)
    stop()
    #turn
    set_dir_servo_angle(40)
    backward(30)
    time.sleep(0.25)
    stop()
    #backup
    set_dir_servo_angle(0)
    backward(30)
    time.sleep(0.5)
    stop()
    print("done Parallel Parking - Left")
    print()


def ParallelParkingRight():
    print("Starting Parallel Parking - Right")
    # turn
    set_dir_servo_angle(40)
    backward(30)
    time.sleep(0.25)
    stop()
    # backup
    set_dir_servo_angle(0)
    backward(30)
    time.sleep(0.5)
    stop()
    # turn
    set_dir_servo_angle(-40)
    backward(30)
    time.sleep(0.25)
    stop()
    # backup
    set_dir_servo_angle(0)
    backward(30)
    time.sleep(0.5)
    stop()

    print("done Parallel Parking - Right")
    print()

def ThreePointTurn():
    print("Starting Three Point Turn")
    #forward
    set_dir_servo_angle(-40)
    time.sleep(0.05)
    forward(50,0)
    time.sleep(0.5)
    stop()
    #backwards
    set_dir_servo_angle(40)
    time.sleep(0.05)
    backward(50)
    time.sleep(0.5)

    #forward
    set_dir_servo_angle(0)
    time.sleep(0.05)
    forward(50,0)
    time.sleep(0.5)
    print("done Three Point Turn")
    print()


while True:
    inp = input("Enter Command[f, pl, pr, 3, q]: ")

    if inp == 'f':
        FwdBack()
    elif inp == 'pl':
        ParallelParkingLeft()
    elif inp == 'pr':
        ParallelParkingRight()
    elif inp == '3':
        ThreePointTurn()
    elif inp == 'q':
        print('Quitting')
        break


