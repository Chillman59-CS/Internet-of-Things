from urllib import request, parse
from time import sleep
from random import randint

# Channel ID: 3509599
# Author: mwa0000042463975
# API KEY (Write): W4XR5FDI49FO6W7F
# API KEY (Read): HCV7XUC0NJCPGLEB

def make_param_thingspeak(data):
    params = parse.urlencode({'field1': data}).encode()
    return params

def thingspeak_post(params):
    api_key_write = "W4XR5FDI49FO6W7F"
    reg = request.Request('https://api.thingspeak.com/update', method="POST")
    reg.add_header("Content-Type", "application/x-www-form-urlencoded")
    reg.add_header("X-THINGSPEAKAPIKEY", api_key_write)
    r = request.urlopen(reg, data = params)
    respone_data = r.read()
    return respone_data

while True:
    data_random = randint(0,50)
    print(data_random)

    params_thingspeak = make_param_thingspeak(data_random)
    thingspeak_post(params_thingspeak)

    sleep(20)