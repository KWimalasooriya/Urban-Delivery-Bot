import RPi.GPIO as GPIO
import time


# GPIO Pin Configurations
# Gear DC Motors (M1, M3, M4, M6)
EA_M1 = 23  # pin 16
EB_M3 = 23
EA_M4 = 24  # pin 18
EB_M6 = 24

IN1_M1 = 25  # pin 22
IN3_M3 = 25
IN1_M4 = 16  # pin 36
IN3_M6 = 16

IN2_M1 = 26  # pin 37
IN4_M3 = 26
IN2_M4 = 27  # pin 13
IN4_M6 = 27

# High RPM Motors (M2, M5)
LE_M2 = 14  # High to 5V
RE_M2 = 15  # High to 5V
LPWM_M2 = 13  # PWM pin 33 for M2
RPWM_M2 = 18  # PWM pin 12 for M2

LE_M5 = 18  # High to 5V
RE_M5 = 19  # High to 5V
LPWM_M5 = 12  # PWM pin 32 for M5
RPWM_M5 = 19  # PWM pin 35 for M5

# Ultrasonic Sensor Pins
FRONT_TRIG = 5 # Pin 29
FRONT_ECHO = 6 # Pin 31
LEFT_TRIG = 20 # Pin 38
LEFT_ECHO = 21 # Pin 40
RIGHT_TRIG = 7 # Pin 26
RIGHT_ECHO = 8 # Pin 24

# GPIO Setup
GPIO.setmode(GPIO.BCM)

# Set gear motor pins as outputs
motor_pins = [EA_M1, EB_M3, EA_M4, EB_M6, IN1_M1, IN3_M3, IN1_M4, IN3_M6, IN2_M1, IN4_M3, IN2_M4, IN4_M6]
GPIO.setup(motor_pins, GPIO.OUT)

# Always HIGH pins
always_high_pins = [EA_M1, EB_M3, EA_M4, EB_M6]
GPIO.output(always_high_pins, GPIO.HIGH)

# Set high RPM motor pins as outputs
high_rpm_pins = [LE_M2, RE_M2, LPWM_M2, RPWM_M2, LE_M5, RE_M5, LPWM_M5, RPWM_M5]
GPIO.setup(high_rpm_pins, GPIO.OUT)

# Initialize PWM for high RPM motors
pwm_m2_l = GPIO.PWM(LPWM_M2, 100)  # 100Hz frequency
pwm_m2_r = GPIO.PWM(RPWM_M2, 100)
pwm_m5_l = GPIO.PWM(LPWM_M5, 100)
pwm_m5_r = GPIO.PWM(RPWM_M5, 100)

pwm_m2_l.start(0)
pwm_m2_r.start(0)
pwm_m5_l.start(0)
pwm_m5_r.start(0)

# Set ultrasonic sensor pins as outputs and inputs
ultrasonic_pins = [(FRONT_TRIG, FRONT_ECHO), (LEFT_TRIG, LEFT_ECHO), (RIGHT_TRIG, RIGHT_ECHO)]
for trig, echo in ultrasonic_pins:
    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)

def measure_distance(trig, echo):
    GPIO.output(trig, GPIO.LOW)
    time.sleep(0.01)
    GPIO.output(trig, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trig, GPIO.LOW)

    start_time = time.time()
    stop_time = time.time()

    while GPIO.input(echo) == 0:
        start_time = time.time()

    while GPIO.input(echo) == 1:
        stop_time = time.time()

    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2  # Distance in cm
    return distance

# Motor Control Functions
def stop_all_motors():
    GPIO.output(motor_pins, GPIO.LOW)
    GPIO.output(always_high_pins, GPIO.HIGH)  # Keep always HIGH pins HIGH
    pwm_m2_l.ChangeDutyCycle(0)
    pwm_m2_r.ChangeDutyCycle(0)
    pwm_m5_l.ChangeDutyCycle(0)
    pwm_m5_r.ChangeDutyCycle(0)
    print("Stopped all motors")

def forward():
    print("Moving forward")
    GPIO.output([IN1_M1, IN1_M4], GPIO.HIGH)
    GPIO.output([IN2_M1, IN2_M4], GPIO.LOW)
    GPIO.output([IN3_M3, IN3_M6], GPIO.HIGH)
    GPIO.output([IN4_M3, IN4_M6], GPIO.LOW)
    pwm_m2_l.ChangeDutyCycle(100)
    pwm_m5_l.ChangeDutyCycle(100)
    pwm_m2_r.ChangeDutyCycle(0)
    pwm_m5_r.ChangeDutyCycle(0)

def backward():
    print("Moving backward")
    GPIO.output([IN1_M1, IN1_M4], GPIO.LOW)
    GPIO.output([IN2_M1, IN2_M4], GPIO.HIGH)
    GPIO.output([IN3_M3, IN3_M6], GPIO.LOW)
    GPIO.output([IN4_M3, IN4_M6], GPIO.HIGH)
    pwm_m2_r.ChangeDutyCycle(100)
    pwm_m5_r.ChangeDutyCycle(100)
    pwm_m2_l.ChangeDutyCycle(0)
    pwm_m5_l.ChangeDutyCycle(0)

def turn_left():
    print("Turning left")
    GPIO.output([IN1_M4, IN3_M6], GPIO.HIGH)
    GPIO.output([IN2_M4, IN4_M6], GPIO.LOW)
    GPIO.output([IN1_M1, IN3_M3], GPIO.LOW)
    GPIO.output([IN2_M1, IN4_M3], GPIO.HIGH)
    pwm_m2_l.ChangeDutyCycle(0)
    pwm_m2_r.ChangeDutyCycle(100)
    pwm_m5_l.ChangeDutyCycle(100)
    pwm_m5_r.ChangeDutyCycle(0)

def turn_right():
    print("Turning right")
    GPIO.output([IN1_M1, IN3_M3], GPIO.HIGH)
    GPIO.output([IN2_M1, IN4_M3], GPIO.LOW)
    GPIO.output([IN1_M4, IN3_M6], GPIO.LOW)
    GPIO.output([IN2_M4, IN4_M6], GPIO.HIGH)
    pwm_m2_l.ChangeDutyCycle(100)
    pwm_m2_r.ChangeDutyCycle(0)
    pwm_m5_l.ChangeDutyCycle(0)
    pwm_m5_r.ChangeDutyCycle(100)

def obstacle_avoidance():
    while True:
        front_distance = measure_distance(FRONT_TRIG, FRONT_ECHO)
        print(f"Front Distance: {front_distance:.2f} cm")

        if front_distance < 50:
            stop_all_motors()
            print("Obstacle detected! Checking sides.")

            left_distance = measure_distance(LEFT_TRIG, LEFT_ECHO)
            right_distance = measure_distance(RIGHT_TRIG, RIGHT_ECHO)

            print(f"Left Distance: {left_distance:.2f} cm, Right Distance: {right_distance:.2f} cm")

            if left_distance > right_distance:
                turn_left()
            else:
                turn_right()

            time.sleep(2)

            # Turn back and move forward
            if left_distance > right_distance:
                turn_right()
            else:
                turn_left()

            time.sleep(2)
            forward()
        else:
            forward()

try:
    obstacle_avoidance()
except KeyboardInterrupt:
    stop_all_motors()
    GPIO.cleanup()
    print("Program terminated.")