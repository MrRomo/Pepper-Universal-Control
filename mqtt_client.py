import paho.mqtt.client as mqtt
import time
# The callback for when a PUBLISH message is received from the server.
def on_message_mqtt(client, userdata, msg):
    print("We got a message!")
    print('%s %s' % (msg.topic, msg.payload))
 
broker_addres = "broker.hivemq.com"
client = mqtt.Client('PC')
client.on_message = on_message_mqtt
client.connect(broker_addres)
client.subscribe("testPepper")
dir(client)
client.loop_forever()   