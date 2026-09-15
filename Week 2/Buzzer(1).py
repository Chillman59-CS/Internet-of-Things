from grove.gpio import GPIO
import sys, time

buzzer_pin = 12 

class GroveBuzzer(GPIO):
    def __init__(self, pin):
        super(GroveBuzzer,self).__init__(pin, GPIO.OUT)
    def on(self):
        self.write(1)
    def off(self):
        self.write(0)
buzzer = GroveBuzzer(buzzer_pin)

while True:
    try:
        buzzer.on()
        time.sleep(0.1)
        buzzer.off()
        time.sleep(1)
    except KeyboardInterrupt:
        buzzer.off()
        print("exit")
        exit(1)
       