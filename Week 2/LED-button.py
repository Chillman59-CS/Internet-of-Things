from gpiozero import LED
from signal import pause

led = LED(5)

led.blink(0.3, 1, 5)    # LED blink 5 times with 0.3s on and 1s off

pause()