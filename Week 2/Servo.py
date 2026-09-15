import RPi.GPIO as GPIO
import time
import sys
from numpy import interp

servo_pin = 12

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

class GroveServo:
    MIN_DEGREE = 0
    MAX_DEGREE = 180
    INIT_DUTY = 2.5

    def __init__(self, channel):
        GPIO.setup(channel, GPIO.OUT)
        self.pwm = GPIO.PWM(channel, 50)
        self.pwm.start(GroveServo.INIT_DUTY)

    def __del__(self):
        self.pwm.stop()

    def setAngle(self, angle):
        # Map angle from range 0-180 to range 25-125
        angle = max(min(angle, GroveServo.MAX_DEGREE), GroveServo.MIN_DEGREE)
        tmp = interp(angle, [0, 180], [25, 125])
        self.pwm.ChangeDutyCycle(round(tmp/10.0, 1))

servo = GroveServo(servo_pin)

while True:
    for x in range(0, 180, 10):
        print(x, "degree")
        servo.setAngle(x)
        time.sleep(0.1)

    for x in range(180, 0, -10):
        print(x, "degree")
        servo.setAngle(x)
        time.sleep(0.1)