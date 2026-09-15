from gpiozero import LED    # Khai bao su dung ham trong thu vien
from time import sleep  # Khai bao thu vien time de dung ham sleep

led = LED(17)    # Khai bao chan GPIO 17 la chan dieu khien led

while True:
    led.on()    # Bat den led
    sleep(1)    # Cho den 1 giay

    led.off()    # Tat den led
    sleep(1)    # Cho den 1 giay