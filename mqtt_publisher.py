import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, rc):
    print('Connected with result code %s' % rc)
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed. There are other methods to achieve this.
    client.subscribe("testPepper")


client = mqtt.Client()
client.on_connect = on_connect

# client.connect("test.mosquitto.org" )
client.connect("169.254.201.28")

for i in range(100):
    client.publish('testPepper', 'CabezaAr')
    print('CabezaAr')
    time.sleep(2)
    client.publish('testPepper', 'CabezaAb')
    print('CabezaAb')
    time.sleep(2)


# publish.single('testPepper', 'ON - PEPPPER', hostname='http://try:try@broker.shiftr.io/example')