from gpiozero import LED
from time import sleep
from urllib import request, parse
import json

# Channel ID: 
# Author: 
# API KEY (Write): 
# API KEY (Read): 

red = LED(5)

def thingspeak_get():
    api_key_red = ""
    channel_id = ""
    req = request.Request("" %(channel_id, api_key_red), method="GET")
    r =request.urlopen(req)
    response_data = r.read().decode()
    respone_data = json.loads(response_data)
    value = respone_data['field1']
    return value

while True:
    value = thingspeak_get()
    print(value)
    if value == "1":
        red.on()
    else:
        red.off()
    