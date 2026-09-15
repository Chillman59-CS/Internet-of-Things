from gpiozero import DistanceSensor    # Khai bao su dung ham trong thu vien
from time import sleep    # Khai bao thu vien time de dung ham sleep

sensor = DistanceSensor(echo=23, trigger=24)

while True:
    print('Distance: ', sensor.distance, 'm')    # In ra khoang cach do duoc
    sleep(1)    # Cho den 1 giay