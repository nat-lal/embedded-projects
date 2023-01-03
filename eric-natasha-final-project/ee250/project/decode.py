import matplotlib.pyplot as plt
import numpy as np
from pydub import AudioSegment
import random
import sys
import os


#Tunable Parameters
lower_fbound = 6000
mid = 8000
upper_fbound = 12000
window = 100
MAX_FRQ = upper_fbound
SLICE_SIZE = 0.25
WINDOW_SIZE = 0.25
char_lookup = [['A','B','C','D','E','F'], 
               ['G','H','I','J','K','L'], 
               ['M','N','O','P','Q','R'], 
               ['S','T','U','V','W','X'],
               ['Y','Z',' ',' ',' ','~']]

#Globals
lowFreqs = list()
highFreqs = list()

#Gets frequency of max FFT
def get_max_frq(frq, fft):
    max_frq = 0
    max_fft = 0
    for idx in range(len(fft)):
        if abs(fft[idx]) > max_fft:
            max_fft = abs(fft[idx])
            max_frq = frq[idx]
    return max_frq


#Finds two FFT peaks in an array
def get_peak_frqs(frq, fft):
    low = int(len(frq)*(lower_fbound/upper_fbound))
    bound = int(len(frq)*(mid/upper_fbound))
    low_frq = frq[low:bound]
    low_frq_fft = fft[low:bound]
    high_frq = frq[bound:]
    high_frq_fft = fft[bound:]

    #spliting the FFT to high and low frequencies
    return (get_max_frq(low_frq, low_frq_fft), get_max_frq(high_frq, high_frq_fft))

#Finds corresponding character from a frequency pair. Returns '?' if not found
def get_char_from_frq(lower_frq, higher_frq):
    low_index = -1; high_index= -1

    for i in range(len(lowFreqs)):
        if (lower_frq < lowFreqs[i]+10) and (lower_frq > lowFreqs[i]-10):
            low_index = i
            break
    
    for i in range(len(highFreqs)):
        if (higher_frq < highFreqs[i]+10) and (higher_frq > highFreqs[i]-10):
            high_index = i
            break

    #print(lower_frq, higher_frq)
    if(low_index == -1 or high_index == -1): return '?'
    return char_lookup[low_index][high_index]

def main(file, key):
    #Seed RNG with key
    random.seed(key)

    #Generate high and low frequencies
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
    
    #Get audio file and properties
    audio = AudioSegment.from_wav(file)
    sample_count = audio.frame_count()
    sample_rate = audio.frame_rate
    samples = audio.get_array_of_samples()
    period = 1/sample_rate                      
    duration = sample_count/sample_rate         

    #Compute Slices
    slice_sample_size = int(SLICE_SIZE*sample_rate)     
    n = slice_sample_size                              
    start_index = 0                                 
    end_index = start_index + slice_sample_size     
    output = ''

    #Generate frequency spectrum
    k = np.arange(n)                                
    slice_duration = n/sample_rate                  
    frq = k/slice_duration                          
    max_frq_idx = int(MAX_FRQ*slice_duration)       
    frq = frq[range(max_frq_idx)]                   
    
    #Main Decoding Loop
    i = 1
    while end_index < len(samples):
        i += 1

        #Grabs slice and performs FFT
        sample_slice = samples[start_index: end_index]
        slice_fft = np.fft.fft(sample_slice)/n
        
        #Truncates FFT slice to frequency range
        slice_fft = slice_fft[range(max_frq_idx)]

        #Calculates locations of upper and lower FFT peaks using get_peak_frqs()
        peak_frqs = get_peak_frqs(frq, slice_fft)

        #Append String
        char = get_char_from_frq(peak_frqs[0], peak_frqs[1])
        if char == '~': break
        output += char

        #Incrementing the start and end window for FFT analysis
        start_index += int(WINDOW_SIZE*sample_rate)
        end_index = start_index + slice_sample_size

    print("Decoded message: " + output)
    
    #Output Analysis Graphs
    x = np.arange(0, duration, (1/sample_rate))
    plt.figure(figsize=(16, 8))
    plt.plot(x, samples)
    plt.xlim(0, 0.25)
    plt.show()
    
    return output
    

if __name__ == '__main__':
    if len(sys.argv) != 3 or not os.path.isfile(sys.argv[1]):
        print("Usage: decode.py [file] [key]")
        exit(1)
    main(sys.argv[1], sys.argv[2])