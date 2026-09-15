from gpiozero import Buzzer 
from signal import pause 

bz = Buzzer(12)
bz.beep(3, 1)

pause()