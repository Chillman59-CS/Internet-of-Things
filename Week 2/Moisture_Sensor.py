import time
from grove.gpio import GPIO
from grove.grove_moisture_sensor import GroveMoistureSensor
from grove.display.jhd1802 import JHD1802

buzzer_pin = 12
MoistureSensor_pin = 0

class GroveBuzzer(GPIO):
    def __init__(self, pin):
        super(GroveBuzzer, self).__init__(pin, GPIO.OUT)
        self.off()

    def on(self):
        self.write(1)

    def off(self):
        self.write(0)

def main():
    lcd = JHD1802()
    buzzer = GroveBuzzer(buzzer_pin)
    sensor = GroveMoistureSensor(MoistureSensor_pin)

    while True:
        moisture = sensor.moisture
        if 0 <= moisture < 300:
            level = "dry"
            buzzer.off()
        elif 300 <= moisture < 700:
            level = "moist"
            buzzer.off()
        else:
            level = "wet"
            buzzer.on()

        print("Moisture: {}, Level: {}".format(moisture, level))

        lcd.setCursor(0, 0)
        lcd.write("Moisture: {0:6}".format(moisture))

        lcd.setCursor(1, 0)
        lcd.write("Level: {0:16}".format(level))

        time.sleep(1)
        
if __name__ == '__main__':
    main()