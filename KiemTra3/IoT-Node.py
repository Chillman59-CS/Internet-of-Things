import time
import sys
import json
from urllib import request, parse, error
from grove.gpio import GPIO
from grove.adc import ADC
from grove.display.jhd1802 import JHD1802

API_KEY = "ZZ67OKFCD3QPSYTF"
TS_URL = "https://api.thingspeak.com/update"
INTERVAL = 20

PIN_BLUE_LED_BUTTON = 18  # Grove - Blue LED Button
PIN_BUZZER = 16
PIN_YELLOW_LED_BUTTON = 5  # Grove - Yellow LED Button
PIN_SERVO = 12
PIN_ULTRASONIC = 22
SENSOR_LIGHT_CHANNEL = 0

class GroveLed(GPIO):
    def __init__(self, pin):
        super(GroveLed, self).__init__(pin, GPIO.OUT)
    def on(self):
        self.write(1)
    def off(self):
        self.write(0)

class GroveBuzzer(GPIO):
    def __init__(self, pin):
        super(GroveBuzzer, self).__init__(pin, GPIO.OUT)
    def on(self):
        self.write(1)
    def off(self):
        self.write(0)

class GroveLightSensor:
    def __init__(self, channel=SENSOR_LIGHT_CHANNEL):
        self.channel = channel
        self.adc = ADC()
    @property
    def light(self):
        return self.adc.read(self.channel)

usleep = lambda x: time.sleep(x / 1000000.0)
_TIMEOUT1 = 1000
_TIMEOUT2 = 10000

class GroveUltrasonicRanger(object):
    def __init__(self, pin):
        self.dio = GPIO(pin)

    def _get_distance(self):
        self.dio.dir(GPIO.OUT)
        self.dio.write(0)
        usleep(2)
        self.dio.write(1)
        usleep(10)
        self.dio.write(0)
        self.dio.dir(GPIO.IN)

        t0 = time.time()
        count = 0
        while count < _TIMEOUT1:
            if self.dio.read():
                break
            count += 1
        if count >= _TIMEOUT1:
            return None

        t1 = time.time()
        count = 0
        while count < _TIMEOUT2:
            if not self.dio.read():
                break
            count += 1
        if count >= _TIMEOUT2:
            return None

        t2 = time.time()
        dt = int((t1 - t0) * 1000000)
        if dt > 530:
            return None

        distance = ((t2 - t1) * 1000000 / 29 / 2)
        return distance

    def get_distance(self):
        for _ in range(5):
            dist = self._get_distance()
            if dist is not None:
                return dist
            time.sleep(0.01)
        return None

class ServoController:
    def __init__(self, pin=PIN_SERVO):
        self.pin = pin
        try:
            import RPi.GPIO as RPIO
            RPIO.setmode(RPIO.BCM)
            RPIO.setup(self.pin, RPIO.OUT)
            self.pwm = RPIO.PWM(self.pin, 50)
            self.pwm.start(0)
        except Exception:
            self.pwm = None

    def set_angle(self, angle):
        angle = max(0, min(180, angle))
        duty = 2.5 + (angle / 180.0) * 10.0
        if self.pwm:
            self.pwm.ChangeDutyCycle(duty)
            time.sleep(0.3)
            self.pwm.ChangeDutyCycle(0)

    def stop(self):
        if self.pwm:
            self.pwm.stop()

def publish_via_http(light_val, dist_val):
    params = {
        "api_key": API_KEY,
        "field1": light_val,
        "field2": f"{dist_val:.1f}" if dist_val is not None else "0.0"
    }
    data = parse.urlencode(params).encode("utf-8")
    req = request.Request(TS_URL, data=data, method="POST")
    try:
        with request.urlopen(req, timeout=5) as response:
            res_text = response.read().decode("utf-8")
            print(f"[HTTP SUCCESS] Entry ID: #{res_text}")
            return res_text
    except Exception as e:
        print(f"[HTTP ERROR]: {e}")
        return None

def main():
    print("DE BAI KIEM TRA SO 5: RASPBERRY PI GIAM SAT ANH SANG VAKHOANG CACH")

    blue_led_btn = GroveLed(PIN_BLUE_LED_BUTTON)
    yellow_led_btn = GroveLed(PIN_YELLOW_LED_BUTTON)
    buzzer = GroveBuzzer(PIN_BUZZER)
    light_sensor = GroveLightSensor(SENSOR_LIGHT_CHANNEL)
    sonar = GroveUltrasonicRanger(PIN_ULTRASONIC)
    servo = ServoController(PIN_SERVO)
    lcd = JHD1802()

    blue_is_on = False
    yellow_is_on = False

    try:
        while True:
            light_val = light_sensor.light
            dist_val = sonar.get_distance()
            if dist_val is None:
                dist_val = 0.0

            if light_val > 300:
                blue_led_btn.on()
                buzzer.on()
                blue_is_on = True
            elif light_val < 660:
                blue_led_btn.off()
                buzzer.off()
                blue_is_on = False

            if dist_val < 30:
                yellow_led_btn.on()
                servo.set_angle(90)
                yellow_is_on = True
            elif dist_val > 50:
                yellow_led_btn.off()
                servo.set_angle(0)
                yellow_is_on = False

            current_time = time.strftime("%H:%M:%S")
            print(f"--- [Time: {current_time}] ---")
            print(f"  + Light: {light_val} | Blue LED Button & Buzzer: {'ON' if blue_is_on else 'OFF'}")
            print(f"  + Dist : {dist_val:.1f} cm | Yellow LED Button & Servo: {'ON' if yellow_is_on else 'OFF'}")

            lcd.setCursor(0, 0)
            lcd.write(f"Light: {light_val:<10}")
            lcd.setCursor(1, 0)
            lcd.write(f"Dist: {dist_val:.1f}cm     ")

            publish_via_http(light_val, dist_val)
            time.sleep(INTERVAL)

    except KeyboardInterrupt:
        blue_led_btn.off()
        yellow_led_btn.off()
        buzzer.off()
        servo.set_angle(0)
        servo.stop()
        lcd.setCursor(0, 0)
        lcd.write("System Stopped  ")
        lcd.setCursor(1, 0)
        lcd.write("                ")
        sys.exit(0)

if __name__ == "__main__":
    main()
