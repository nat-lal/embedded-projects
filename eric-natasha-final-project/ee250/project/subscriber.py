
import paho.mqtt.client as mqtt
import time
import encode
import publisher

key = str
message = str
audio_send = False

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    #submit topic only subscribed to when the button is pressed and a letter is selected
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

def msg_callback(client,userdata, msg): #submits message
    print("Submitted message value: {}".format(str(msg.payload, "utf-8")))
    global message
    message = str(msg.payload, "utf-8")

def key_callback(client,userdata, msg): #submits key
    print("Submitted key value: {}".format(str(msg.payload, "utf-8")))
    global key
    key = str(msg.payload, "utf-8")
    global audio_send
    audio_send = True
    

if __name__ == '__main__':
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=1883, keepalive=60)
    client.loop_start()

    while True:
        time.sleep(1)
        if audio_send:
            break
    
    if audio_send:
        encode.main(key, message)
        print("Audio Generated")
        publisher.sendAudio("output.wav")
        print("Audio Sent")

