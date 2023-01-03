
import paho.mqtt.client as mqtt
import time
import sys

sys.path.append('../../Software/Python/')
sys.path.append('../../Software/Python/grove_rgb_lcd')

import grovepi
from grove_rgb_lcd import *

def on_connect(client, userdata, flags, rc):
    print("Connected to server (i.e., broker) with result code "+str(rc))

    client.subscribe("en/lcd")
    client.message_callback_add("en/lcd", lcd_callback) #This is for the LCD callback

def on_message(client, userdata, msg):
    print("on_message: " + msg.topic + " " + str(msg.payload, "utf-8"))

def lcd_callback(client, userdata, msg):
    letter = str(msg.payload, "utf-8")
    print("on_message: " + msg.topic + " " + letter)
    print("Printing to screen.")
    setText(letter + " ")

if __name__ == '__main__':

    client = mqtt.Client()
    client.on_message = on_message
    client.on_connect = on_connect
    client.connect(host="eclipse.usc.edu", port=1883, keepalive=60)
    client.loop_start()

    #input ports
    butPORT = 3
    enPORT = 0

    grovepi.pinMode(butPORT,"INPUT")
    grovepi.pinMode(enPORT, "INPUT")

    state = 0 #states for lcd
    letter = "A" 
    message = "" #eventual message to be sent
    num = 0 #eventual key to be sent


    while True:
        time.sleep(0.1)
        if (state == 0): #state 1: write a message using the encoder
            setRGB(219, 46, 130)
            setText_norefresh("Insert a msg:   " + message + letter)
            pos = grovepi.analogRead(enPORT)
            if (pos <= 39):
                letter = "A"
            elif (pos > 39 and pos <= 78):
                letter = "B"
            elif (pos > 78 and pos <= 117):
                letter = "C"
            elif (pos > 117 and pos <= 156):
                letter = "D"
            elif (pos > 156 and pos <= 195):
                letter = "E"
            elif (pos > 195 and pos <= 234):
                letter = "F"
            elif (pos > 234 and pos <= 273):
                letter = "G"
            elif (pos > 273 and pos <= 312):
                letter = "H"
            elif (pos > 312 and pos <= 351):
                letter = "I"
            elif (pos > 351 and pos <= 390):
                letter = "J"
            elif (pos > 390 and pos <= 429):
                letter = "K"
            elif (pos > 429 and pos <= 468):
                letter = "L"
            elif (pos > 468 and pos <= 507):
                letter = "M"
            elif (pos > 507 and pos <= 546):
                letter = "N"
            elif (pos > 546 and pos <= 585):
                letter = "O"
            elif (pos > 585 and pos <= 624):
                letter = "P"
            elif (pos > 624 and pos <= 663):
                letter = "Q"
            elif (pos > 663 and pos <= 702):
                letter = "R"
            elif (pos > 702 and pos <= 741):
                letter = "S"
            elif (pos > 741 and pos <= 780):
                letter = "T"
            elif (pos > 780 and pos <= 819):
                letter = "U"
            elif (pos > 819 and pos <= 858):
                letter = "V"
            elif (pos > 858 and pos <= 897):
                letter = "W"
            elif (pos > 897 and pos <= 936):
                letter = "X"
            elif (pos > 936 and pos <= 975):
                letter = "Y"
            elif (pos > 975 and pos <= 1000):
                letter = "Z"
            elif (pos > 1000 and pos <= 1022):
                letter = " "
            else:
                letter = "^"
        elif (state == 1): #state 1: choose a key with the encoder
            setRGB(197, 101, 252)
            setText_norefresh("Insert a num:   " + str(num))
            if (grovepi.analogRead(enPORT) <= 1000):
                num = grovepi.analogRead(enPORT)
            else:
                num = 1000
        elif (state == 2): #state 2: both the msg and key have been submitted
            setRGB(90, 204, 214)
            setText_norefresh("Waiting...")

        if (grovepi.digitalRead(butPORT) == 1 and state == 0):
            if (letter != "^"): #ensure that the end char doesn't get added
                message += letter
            if (len(message) == 15 or letter == "^"): #if msg is 15, autosend
                #client.publish("en/submit", message)
                client.publish("en/msgsubmit", message)
                state = 1
        elif (grovepi.digitalRead(butPORT) == 1 and state == 1):
            #client.publish("en/submit", str(num))
            client.publish("en/keysubmit", str(num))
            state = 2
                


