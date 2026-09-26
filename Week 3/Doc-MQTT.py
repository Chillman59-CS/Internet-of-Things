from paho.mqtt.enums import CallbackAPIVersion
import paho.mqtt.client as mqtt
from time import sleep

# Channel ID: 3509599
# Username: NjkPID0mNzk1FxAPMCwoAyE
# ClientID: NjkPID0mNzk1FxAPMCwoAyE
# Password: 0S20gMqwBsJUlVoS1w+rbuFE

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected with result code {}".format(reason_code))
    channel_ID = "3509599"

    client.subscribe("channels/%s/subscribe/fields/field2" %(channel_ID))

def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    print("Disconnected from Broker")

def on_message(client, userdata, message):
    print(message.payload.decode())
    print(message.topic)

client_id = "NjkPID0mNzk1FxAPMCwoAyE"
client = mqtt.Client(
    callback_api_version=CallbackAPIVersion.VERSION2,
    client_id=client_id,
)

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_message = on_message
client.username_pw_set(username="NjkPID0mNzk1FxAPMCwoAyE", password="0S20gMqwBsJUlVoS1w+rbuFE")
client.connect("mqtt3.thingspeak.com", 1883, 60)
client.loop_forever()