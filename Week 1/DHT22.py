import Adafruit_DHT # Khai bao su dung ham trong thu vien

sensor = Adafruit_DHT.DHT22 # Chon loai cam bien (DHT11, DHT22, AM2302)
gpio = 16 # Chon chan GPIO de ket noi cam bien

print("Please wait, reading sensor data...") # In ra thong bao cho nguoi dung biet

humidity, temperature = Adafruit_DHT.read_retry(sensor, gpio) # Doc du lieu tu cam bien

if humidity is not None and temperature is not None: # Kiem tra du lieu co hop le hay khong
    print('Temp = {0:0.1f}*C  Humidity = {1:0.1f}%'.format(temperature, humidity)) # In ra nhiet do va do am
else:
    print('Failed to get reading. Try again!') # In ra thong bao loi neu khong doc duoc du lieu