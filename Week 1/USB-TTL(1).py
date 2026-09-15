from time import sleep  # Khai bao thu vien time de dung ham sleep
import serial    # Khai bao su dung ham trong thu vien

ser = serial.Serial('/dev/ttyS0', 9600, serial.PARITY_NONE, serial.STOPBITS_ONE, serial.EIGHTBITS, timeout=1)

print("Raspberry Pi's sending: ")

try:
    while True:
        transmit_data = "36-Be-Xo"    # Nhan du lieu tu ban phim
        ser.write(transmit_data)    # Gui du lieu qua Port noi tiep
        ser.write("\n")
        print(transmit_data)    # In ra du lieu gui di
        sleep(1)    # Cho den 1 giay
except KeyboardInterrupt:
    print("Exiting...")
    ser.close()    # Dong cong USB khi ket thuc chuong trinh
    print("Program stopped by user.")