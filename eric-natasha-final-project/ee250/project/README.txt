PROJECT README
Eric Zhong and Natasha Lal


Instructions on compiling and executing programs:
The encode.py and decode.py files are used to perform the message encoding and decoding for the audio files. 
encode.py creates a .wav file with the encoded message while decode outputs the decoded message after reading in
the target .wav file. The encode program is additionally referenced within the VM mqtt scripts. Both commands 
can be run from the terminal as follows:
encode.py [key] [message] [output file (optional)]
decode.py [file] [key]

The rpi.py should be run on the rpi while the subscriber.py should be run at the same time on the VM. This 
provides the necessary MQTT functionality for the user to send the message and key from the RPi to the VM 
and for the VM to send the audio array back to the RPi to play. The publisher.py procedures are called from 
subscriber.py once the audio file is ready to send.

The dev.ipynb notebook file was used for dev purposes only and is not actively used in the final product. Any
desired testing/tweaking can be tested in the notebook.


External Libraries Used:
sys
numpy
matplotlib
pydub
random
wave
wavio
paho mqtt
time
playsound