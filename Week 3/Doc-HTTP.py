from urllib import request, parse
from time import sleep
import json

# Channel ID: 3509599
# Author: mwa0000042463975
# API KEY (Write): W4XR5FDI49FO6W7F
# API KEY (Read): HCV7XUC0NJCPGLEB

def thingspeak_get():
    api_key_read = "HCV7XUC0NJCPGLEB"
    channel_ID = "3509599"
    req = request.Request("https://api.thingspeak.com/channels/%s/fields/1/last.json?api_key=%s" % (channel_ID, api_key_read), method="GET")
    r = request.urlopen(req)
    respone_data = r.read().decode()
    respone_data = json.loads(respone_data)
    value = respone_data['field1']
    return value

value = thingspeak_get()
print(value)