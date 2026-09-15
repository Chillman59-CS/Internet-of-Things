import time
from grove.display.jhd1802 import JHD1802

lcd = JHD1802()

lcd.setCursor(0, 0)
lcd.write("Len con phim 36 ")

time.sleep(1)

lcd.setCursor(1, 0)
lcd.write("I Hate Nigga    ")