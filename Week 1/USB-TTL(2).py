import serial    # Khai bao su dung ham trong thu vien

ser = serial.Serial('/dev/ttyUSB0', 9600, serial.PARITY_NONE, serial.STOPBITS_ONE, serial.EIGHTBITS, timeout=1)

print("Raspberry Pi's receiving: ")

try:
    while True:
        s = ser.readline()    # Cho doi (timeout) de doc du lieu tu Port noi tiep
        data = s.decode()   # Giai ma chuoi du lieu
        data = data.strip()   # Loai bo khoang trang o dau va cuoi chuoi
        print(data)    # In ra du lieu nhan duoc
except KeyboardInterrupt:
    print("Exiting...")
    ser.close()    # Dong cong USB