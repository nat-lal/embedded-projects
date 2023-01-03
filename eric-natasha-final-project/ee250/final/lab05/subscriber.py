
import paho.mqtt.client as mqtt
import time
import encode
import decode

key = ""
message = ""

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #button and encoder topics were for testing
    client.subscribe("en/button")
    client.message_callback_add("en/button", button_callback)
    client.subscribe("en/encoder")
    client.message_callback_add("en/encoder", en_callback)

    #submit topic only subscribed to when the button is pressed and a letter is selected
    client.subscribe("en/submit")
    client.message_callback_add("en/submit", submit_callback)
    client.subscribe("en/keysubmit")
    client.message_callback_add("en/keysubmit", key_callback)
    client.subscribe("en/msgsubmit")
    client.message_callback_add("en/msgsubmit", msg_callback)

def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def button_callback(client, userdata, msg):
    print(str(msg.payload, "utf-8"))

def en_callback(client, userdata, msg):
    print("Position: {}".format(str(msg.payload, "utf-8")))

def submit_callback(client,userdata, msg): #submits message and key
    print("Submitted value: {}".format(str(msg.payload, "utf-8")))

def key_callback(client,userdata, msg): #submits key
    print("Submitted key value: {}".format(str(msg.payload, "utf-8")))
    key = str(msg.payload, "utf-8")

def msg_callback(client,userdata, msg): #submits message
    print("Submitted message value: {}".format(str(msg.payload, "utf-8")))
    message = str(msg.payload, "utf-8")
    

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=1883, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(1)
            

