from grove.gpio import GPIO
import sys, time

relay_pin = 12 

class Groverelay(GPIO):
    def __init__(self,pin):
        super(Groverelay, self).__init__(pin, GPIO.OUT)
    def on(self):
            self.write(1)
    def off(self):
            self.write(0)
relay = Groverelay(relay_pin)

while True:
    try:
        relay.on()
        time.sleep(1)
        relay.off()
        time.sleep(1)

    except KeyboardInterrupt:
        relay.off()
        print("exit")
        exit(1)