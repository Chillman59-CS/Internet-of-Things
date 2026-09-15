from time import sleep
from grove.adc import ADC

sensor = ADC()

while True:
    value = sensor.read_voltage(0)
    # value = sensor.read_raw(0)
    # value = sensor.read(0)
    print("ADC Value: {}".format(value))
    sleep(2)