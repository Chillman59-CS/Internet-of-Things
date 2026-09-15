import time, sys, math
import RPi.GPIO as GPIO
from numpy import interp
from grove.adc import ADC

servo_pin = 12
sensor_pin = 0

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

class GroveLightSensor:
    def __init__(self, channel):
        self.adc = ADC()
        self.channel = channel

    @property
    def light(self):
        value = self.adc.read(self.channel)
        return value

servo = GroveServo(servo_pin)
sensor = GroveLightSensor(sensor_pin)

while True:
    angle = sensor.light * 180 / 1000
    print("Light value {}, turn to {} degree".format(sensor.light, angle))
    time.sleep(1)