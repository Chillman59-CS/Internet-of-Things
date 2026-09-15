import serial    # Khai bao su dung ham trong thu vien
from time import sleep  # Khai bao thu vien time de dung ham sleep

ser = serial.Serial('/dev/ttyUSB0', 9600)    # Mo cong voi toc do 9600 baud
# ser = serial.Serial(port='/dev/ttyUSB0', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

while True:
    received_data = ser.read()    # Doc du lieu tu cong USB
    sleep(0.03)    # Cho den 30ms

    data_left = ser.inWaiting()    # Kiem tra xem co du lieu con lai khong
    received_data += ser.read(data_left)    # Doc du lieu con lai

    print(received_data)    # In ra du lieu nhan duoc
    ser.write(received_data)    # Gui du lieu nhan duoc ve cong USB