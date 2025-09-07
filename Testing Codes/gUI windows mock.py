from tkinter import Tk, Button, Label

# Mock GPIO for Windows
class MockGPIO:
    BCM = "BCM"
    OUT = "OUT"
    LOW = "LOW"
    HIGH = "HIGH"

    def setmode(self, mode):
        print(f"Set GPIO mode to {mode}")

    def setup(self, pins, mode):
        print(f"Setup pins {pins} as {mode}")

    def output(self, pins, state):
        print(f"Set pins {pins} to state {state}")

    def cleanup(self):
        print("Cleaned up GPIO")

    class PWM:
        def __init__(self, pin, frequency):
            self.pin = pin
            self.frequency = frequency

        def start(self, duty_cycle):
            print(f"Started PWM on pin {self.pin} with duty cycle {duty_cycle}%")

        def ChangeDutyCycle(self, duty_cycle):
            print(f"Changed PWM duty cycle on pin {self.pin} to {duty_cycle}%")

        def stop(self):
            print(f"Stopped PWM on pin {self.pin}")

# Use MockGPIO on Windows
GPIO = MockGPIO()

# Pin Configurations (as in the original code)
# Pin definitions...
motor_pins = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
high_rpm_pins = [14, 15, 16, 17, 18, 19, 20, 21]

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(motor_pins, GPIO.OUT)
GPIO.setup(high_rpm_pins, GPIO.OUT)

# Initialize PWM for high RPM motors
pwm_m2_l = GPIO.PWM(16, 100)
pwm_m2_r = GPIO.PWM(17, 100)
pwm_m5_l = GPIO.PWM(20, 100)
pwm_m5_r = GPIO.PWM(21, 100)

pwm_m2_l.start(0)
pwm_m2_r.start(0)
pwm_m5_l.start(0)
pwm_m5_r.start(0)

# Motor Control Functions
def stop_all_motors():
    GPIO.output(motor_pins, GPIO.LOW)
    pwm_m2_l.ChangeDutyCycle(0)
    pwm_m2_r.ChangeDutyCycle(0)
    pwm_m5_l.ChangeDutyCycle(0)
    pwm_m5_r.ChangeDutyCycle(0)
    print("Stopped all motors")

def forward():
    print("Moving forward")
    GPIO.output([6, 8], GPIO.HIGH)
    GPIO.output([10, 12], GPIO.LOW)
    GPIO.output([7, 9], GPIO.HIGH)
    GPIO.output([11, 13], GPIO.LOW)
    pwm_m2_l.ChangeDutyCycle(75)
    pwm_m5_l.ChangeDutyCycle(75)

def backward():
    print("Moving backward")
    GPIO.output([6, 8], GPIO.LOW)
    GPIO.output([10, 12], GPIO.HIGH)
    GPIO.output([7, 9], GPIO.LOW)
    GPIO.output([11, 13], GPIO.HIGH)
    pwm_m2_r.ChangeDutyCycle(75)
    pwm_m5_r.ChangeDutyCycle(75)

def turn_left():
    print("Turning left")
    GPIO.output([6, 7], GPIO.HIGH)
    GPIO.output([10, 11], GPIO.LOW)
    pwm_m2_l.ChangeDutyCycle(100)

def turn_right():
    print("Turning right")
    GPIO.output([8, 9], GPIO.HIGH)
    GPIO.output([12, 13], GPIO.LOW)
    pwm_m2_r.ChangeDutyCycle(100)

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
forward_btn = Button(root, text="▲", **button_style, bg="#16A085")
forward_btn.bind("<ButtonPress-1>", lambda event: (on_button_press(forward_btn, "#1ABC9C"), forward()))
forward_btn.bind("<ButtonRelease-1>", lambda event: on_button_release(forward_btn))

backward_btn = Button(root, text="▼", **button_style, bg="#E74C3C")
backward_btn.bind("<ButtonPress-1>", lambda event: (on_button_press(backward_btn, "#C0392B"), backward()))
backward_btn.bind("<ButtonRelease-1>", lambda event: on_button_release(backward_btn))

left_btn = Button(root, text="◀", **button_style, bg="#3498DB")
left_btn.bind("<ButtonPress-1>", lambda event: (on_button_press(left_btn, "#2980B9"), turn_left()))
left_btn.bind("<ButtonRelease-1>", lambda event: on_button_release(left_btn))

right_btn = Button(root, text="▶", **button_style, bg="#F39C12")
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