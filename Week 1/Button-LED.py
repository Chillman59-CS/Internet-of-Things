from gpiozero import LED, Button    # Khai bao su dung ham trong thu vien
from signal import pause    # Khai bao thu vien signal de dung chuong trinh

led = LED(17)    # Khai bao chan GPIO 17 la chan dieu khien led
button = Button(2)    # Khai bao chan GPIO 2 la chan nhan

button.when_pressed = led.on    # Khi nut duoc nhan thi bat den led
button.when_released = led.off    # Khi nut duoc tha ra thi tat den led

pause()    # Vong lap chuong trinh de cho nut nhan va led hoat dong