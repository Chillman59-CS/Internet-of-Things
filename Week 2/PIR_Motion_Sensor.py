import time
from grove.grove_mini_pir_motion_sensor import GroveMiniPIRMotionSensor
from grove.grove_relay import GroveRelay

# Grove - mini PIR Motion Sensor connected to digital port D5
sensor = GroveMiniPIRMotionSensor(5)

# Grove - Relay connected to digital port D16
relay = GroveRelay(16)

def on_detected():
    print("Motion detected!")

    relay.on()
    print("Relay turned on.")

    time.sleep(0.1)  # Keep the relay on for 5 seconds
    
    relay.off()
    print("Relay turned off.")

sensor.on_detected = on_detected

while True:
    time.sleep(1)  # Sleep for a short time to reduce CPU usage