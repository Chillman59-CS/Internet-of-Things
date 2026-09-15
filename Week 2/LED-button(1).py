from grove.gpio import GPIO
import sys, time

led_pin = 5

class GroveLed(GPIO):
    def __init__(self, pin):
        super(GroveLed, self).__init__(pin, GPIO.OUT)

    def on(self): 
        self.write(1)

    def off(self):
        self.write(0)

Led = GroveLed(led_pin)

while True:
    try:
        Led.on()
        time.sleep(1)
        Led.off()
        time.sleep(1)
    except KeyboardInterrupt:
        Led.off()
        print("exit")
        exit(1)