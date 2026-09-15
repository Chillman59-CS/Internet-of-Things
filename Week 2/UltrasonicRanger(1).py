import time 
from grove.grove_relay import GroveRelay
from grove.grove_ultrasonic_ranger import GroveUltrasonicRanger

#Grove - Ultrasonic Ranger connected to port D5
sensor = GroveUltrasonicRanger(5)

#grove - Relay connected to port D16
relay = GroveRelay(16)

while True:
    distance = sensor.get_distance()
    print('{} cm'.format(distance))

    if distance < 20:
        relay.on()
        print('relay on')
    else:
        relay.off()
        print('relay off')
    time.sleep(1)