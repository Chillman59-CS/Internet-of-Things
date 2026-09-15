from gpiozero import LED, Button
from signal import pause

led = LED(5)
button = Button(6)

button.when_pressed = led.on
button.when_released = led.off

pause()