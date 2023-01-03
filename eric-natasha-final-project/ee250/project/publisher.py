
import paho.mqtt.client as mqtt
from pydub import AudioSegment
import time

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

def on_publish(client, userdata, message):
    #the third argument is 'message' here unlike 'msg' in on_message 
    print("Publishing")

def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))



def sendAudio(file):

    client = mqtt.Client()
    client.connect(host="eclipse.usc.edu", port=1883, keepalive=60)
    #client.on_message = on_message
    #client.on_connect = on_connect
    client.loop_start()

    audio = AudioSegment.from_wav(file)
    samples = audio.get_array_of_samples()

    msg = ""
    for s in samples:
        msg += str(s)
        msg += str(',')
    msg = msg[:(len(msg)-1)]
    client.publish("audio", msg)
    time.sleep(1)

