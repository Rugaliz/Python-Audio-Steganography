#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 15:38:32 2020

@author: rugaliz
"""

import os                               # Library for issuing system comands
import multiprocessing                  # Library for multiprocessing
import sys                              # Library for passing system arguments
from scipy.io.wavfile import read       # Scipy library for wave manipulation functions
from scipy.io.wavfile import write

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):              # Function to convert a string into a binary string
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))

def mess_enc_LSB (message_bin, samplerate, audio_out, audio_data = []):        # Function to encode a message using least significant bit method
    for idx in range(0, len(message_bin) - 1):
        audio_data_bin = list (bin (audio_data [100 + idx, 0]))                # first converto to bin string then to list to be more easily manipulated. Uses 0 colum index so as to work with mono or stereo and above.
        audio_data_bin [-1] = message_bin [idx]                                # change last char in list to bit in message to hide
        audio_data_bin_str = "".join(audio_data_bin)                           # revert list to string
        audio_data [100 + idx, 0] = int(audio_data_bin_str, 2)                 # convert string to int and add it back to the dataset
    write(audio_out, samplerate, audio_data)

if __name__ == "__main__":                                                     # confirms that the code is under main function
    message_input = sys.argv[1]
    #message_input = input ('Insert message to code: ')                         # gets the input message
    message_str = " **##**" + " " + message_input + " " +"##**## "             # adds a prefix and sufix for the decoder to find the begining and end of the message. extra spaces are for compatibility with non latin characters (kind of a hack)
    message_bin = text_to_bits(message_str)                                    # message converted to binary
    message_bin_length = len(message_bin)                                      # length of the message already in binary
    
    audio_in =  sys.argv[2]                 # audio input argument
    audio_out = sys.argv[3]                 # audio output argument

    file_data = read(audio_in)              # Scipy function to import audio as data
    samplerate = int(file_data[0])
    audio_data = []
    audio_data = file_data[1].copy()        # need this ".copy()" shenanigans or else the data becomes read only for some reason
    
    thread1 = multiprocessing.Process(target=mess_enc_LSB, args = (message_bin, samplerate, audio_out, audio_data))
    thread1.start()
    thread1.join() 
    os.system("clear")  # clean messy results
    print("Encoding complete!")
