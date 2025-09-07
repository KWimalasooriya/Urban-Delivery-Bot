import RPi.GPIO as GPIO
from tkinter import Tk, Button, Label

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

def quit_program():
    print("Exiting program")
    stop_all_motors()
    GPIO.cleanup()
    root.destroy()

# GUI Setup
root = Tk()
root.title("Six-Wheel Robot Control")
root.configure(bg="#1A1A1D")  # Dark tech background color

# Button Styling with Techy look
button_style = {
    "font": ("Arial", 16, "bold"),
    "width": 10,
    "height": 2,
    "relief": "raised",
    "bd": 5,
    "fg": "#FFFFFF",  # White text color
}

def on_button_press(button, color):
    button.configure(bg=color, relief="sunken")

def on_button_release(button):
    button.configure(bg="#2C3E50", relief="raised")  # Dark blue-gray on release
    stop_all_motors()

# Buttons with more modern and techy color scheme
forward_btn = Button(root, text="?", **button_style, bg="#16A085")
forward_btn.bind("<ButtonPress-1>", lambda event: (on_button_press(forward_btn, "#1ABC9C"), forward()))
forward_btn.bind("<ButtonRelease-1>", lambda event: on_button_release(forward_btn))

backward_btn = Button(root, text="?", **button_style, bg="#E74C3C")
backward_btn.bind("<ButtonPress-1>", lambda event: (on_button_press(backward_btn, "#C0392B"), backward()))
backward_btn.bind("<ButtonRelease-1>", lambda event: on_button_release(backward_btn))

left_btn = Button(root, text="?", **button_style, bg="#3498DB")
left_btn.bind("<ButtonPress-1>", lambda event: (on_button_press(left_btn, "#2980B9"), turn_left()))
left_btn.bind("<ButtonRelease-1>", lambda event: on_button_release(left_btn))

right_btn = Button(root, text="?", **button_style, bg="#F39C12")
right_btn.bind("<ButtonPress-1>", lambda event: (on_button_press(right_btn, "#F1C40F"), turn_right()))
right_btn.bind("<ButtonRelease-1>", lambda event: on_button_release(right_btn))

stop_btn = Button(root, text="STOP", **button_style, bg="#E74C3C", command=stop_all_motors)
quit_btn = Button(root, text="QUIT", **button_style, bg="#34495E", command=quit_program)

# Layout
forward_btn.grid(row=0, column=1, padx=10, pady=10)
left_btn.grid(row=1, column=0, padx=10, pady=10)
stop_btn.grid(row=1, column=1, padx=10, pady=10)
right_btn.grid(row=1, column=2, padx=10, pady=10)
backward_btn.grid(row=2, column=1, padx=10, pady=10)
quit_btn.grid(row=3, column=1, padx=10, pady=10)

# Title Label with techy font and color
Label(root, text="Robirds Corporation", font=("Arial", 18, "bold"), fg="#ECF0F1", bg="#1A1A1D").grid(row=4, column=0, columnspan=3, pady=10)

# Key bindings for keyboard control
def on_key_press(event):
    if event.keysym == "Up":
        forward()
    elif event.keysym == "Down":
        backward()
    elif event.keysym == "Left":
        turn_left()
    elif event.keysym == "Right":
        turn_right()

def on_key_release(event):
    stop_all_motors()

# Bind keyboard events
root.bind("<KeyPress>", on_key_press)
root.bind("<KeyRelease>", on_key_release)

root.mainloop()

