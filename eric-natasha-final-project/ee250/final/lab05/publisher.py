
import paho.mqtt.client as mqtt
import time
from pynput import keyboard

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

def on_publish(client, userdata, message):
    #the third argument is 'message' here unlike 'msg' in on_message 
    print("Publishing")

def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def on_press():
    #try: 
    #    k = key.char # single-char keys
    #except: 
    #    k = key.name # other keys
    k = input("Enter a key: ")
    
    if k == 'w':
        print("w")
        #send "w" character to rpi
        client.publish("en/lcd", "w")
    elif k == 'a':
        print("a")
        # send "a" character to rpi
        client.publish("en/led", "LED ON")
        client.publish("en/lcd", "a")
    elif k == 's':
        print("s")
        # send "s" character to rpi
        client.publish("en/lcd", "s")
    elif k == 'd':
        print("d")
        # send "d" character to rpi
        client.publish("en/led", "LED OFF")
        client.publish("en/lcd", "d")

if __name__ == '__main__':
    #setup the keyboard event listener
    #lis = keyboard.Listener(on_press=on_press)
    #lis.start() # start to listen on a separate thread

    #this section is covered in publisher_and_subscriber_example.py
    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    time.sleep(1)
    client.on_publish = on_publish
    client.connect(host="eclipse.usc.edu", port=1883, keepalive=60)
    client.loop_start()

    while True:
        print("waiting for keystrokes...")
        time.sleep(0.1)
        #on_press()
        #on_sound("../../../Downloads/PinkPanther30.wav")
            

