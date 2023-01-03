import matplotlib.pyplot as plt
import numpy as np
import wavio
import random
import os
import sys

#Tunable Parameters
lower_fbound = 6000
mid = 8000
upper_fbound = 12000
window = 100
char_lookup = [['A','B','C','D','E','F'], 
              ['G','H','I','J','K','L'], 
              ['M','N','O','P','Q','R'], 
              ['S','T','U','V','W','X'],
              ['Y','Z',' ',' ',' ','~']]


#Main Function
def main(key, message, outputFile = "output.wav"):
    #MIntialization/Setup
    originalMessage = message
    message = message.upper()
    random.seed(key)

    #Generate high and low frequencies
    lowFreqs = list()
    for i in range(5):
        while True:
            temp = random.randint(lower_fbound, mid-window)
            flag = True
            for f in lowFreqs:
                if(temp >= f-window and temp <= f+window):
                    flag = False
            if flag:
                break
        lowFreqs.append(temp)
    highFreqs = list()
    for i in range (6):
        while True:
            temp = random.randint(mid+window, upper_fbound)
            flag = True
            for f in lowFreqs:
                if(temp >= f-window and temp <= f+window):
                    flag = False
            if flag:
                break
        highFreqs.append(temp)

    #Message Padding/Trimming
    if len(message) > 15:
        message = message[:16]
    pad = 15-len(message)
    message += '~'
    while pad > 0:
        message += char_lookup[random.randint(0,4)][random.randint(0,5)]
        pad -= 1
    
    #Get frequencies for characters in message
    toneFreqs = list()
    for i in range(len(message)):
        char = message[i]
        freq = tuple()
        if char == '~':
            freq = (lowFreqs[4], highFreqs[5])
        elif char == ' ':
            freq = (lowFreqs[4], highFreqs[2])
        else:
            freq = (lowFreqs[int((ord(char)-ord('A'))/6)], highFreqs[(ord(char)-ord('A'))%6])
        toneFreqs.append(freq)

    #Generate tone from frequencies
    tones = list()
    x = np.arange(0, 0.25, (1/44100))
    for t in toneFreqs:
        tones.append((np.sin(2*np.pi*x * t[0]) + np.sin(2*np.pi*x * t[1]))*0.5)
    output = np.concatenate(tones)

    #Plot Message Waveform
    x = np.arange(0, 4, (1/44100))
    plt.figure(figsize=(16, 8))
    plt.plot(x, output)
    plt.xlim(0, 0.25)
    
    #Write Audio File
    wavio.write(outputFile, output, 44100, sampwidth=4)
    print("Message: '" + originalMessage + "' encoded in " + outputFile + " using key: " + str(key))
    plt.show()


#Check system arguments and execute main
if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: encode.py [key] [message] [output file(optional)]")
        exit(1)
    try:
        int(sys.argv[1])
    except ValueError:
        print("Usage: encode.py [key] [message] [output file(optional)]")
        exit(1)

    for c in sys.argv[2]:
        if not sys.argv[2].isalpha() and sys.argv[2].isspace():
            print("Can only encode letters and spaces up to 15 characters")
            exit(1)
    
    if(len(sys.argv) == 4):
        main(int(sys.argv[1]), sys.argv[2], sys.argv[3])
    else:
        main(int(sys.argv[1]), sys.argv[2])