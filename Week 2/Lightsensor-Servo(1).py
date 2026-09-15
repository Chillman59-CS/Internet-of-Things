import time
from grove.grove_servo import GroveServo
from grove.grove_light_sensor_v1_2 import GroveLightSensor

def main():
    servo = GroveServo(12)
    sensor = GroveLightSensor(0)

    while True:
        angle = sensor.light * 180 / 1000
        print("Light value {}, turn to {} degree".format(sensor.light, angle))
        servo.setAngle(angle)
        time.sleep(1)

if __name__ == '__main__':
    main()