import paho.mqtt.client as mqtt
from paho.mqtt.enums import CallbackAPIVersion
from time import sleep
from random import randint

# Channel ID: 3509599
# Username: NjkPID0mNzk1FxAPMCwoAyE
# ClientID: NjkPID0mNzk1FxAPMCwoAyE
# Password: 0S20gMqwBsJUlVoS1w+rbuFE

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,client_id="Python_Publisher_3509599")
client.username_pw_set(username="NjkPID0mNzk1FxAPMCwoAyE", password="0S20gMqwBsJUlVoS1w+rbuFE")
client.connect("mqtt3.thingspeak.com",1883, 60 )

def thingspeak_mqtt(data):
    channel_ID = "3509599"
    client.publish("channels/%s/publish" %(channel_ID), "field2=%s&status=MQTTPUBLISH" %(data))

while True:
    data_random = randint(0,50)
    print(data_random)

    thingspeak_mqtt(data_random)
    sleep(20)