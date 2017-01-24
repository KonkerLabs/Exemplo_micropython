
import paho.mqtt.client as mqtt
import json
import pprint

with open('konker.config', 'r') as config_file:
    config = json.load(config_file)
    #pprint.pprint(config)
    config_file.close()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    print("(Re)Connected with result code "+str(rc))
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe(config["SUB"])

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to channel. Return codes: ", mid, granted_qos)
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("Topic: ", msg.topic + "\n Message: " +str(msg.payload))

def on_disconnect(client, userdata, rc):
    print("Disconnected with result code "+str(rc))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.on_subscribe = on_subscribe
client.on_disconnect = on_disconnect

client.username_pw_set(config["USER"], config["PWD"])
client.connect(config["URL"], config["PORT"], 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()

