from gpiozero import Button    # Khai bao su dung ham trong thu vien

button = Button(2)    # Khai bao chan GPIO 2 la chan nhan nut

while True:
    if button.is_pressed:    # Kiem tra nut co duoc nhan hay khong
        print("Button is pressed")    # In ra thong bao khi nut duoc nhan
    else:
        print("Button is not pressed")    # In ra thong bao khi nut khong duoc nhan