#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 17 15:38:44 2020

@author: rugaliz
"""


import multiprocessing                  # Library for multiprocessing
import sys                              # Library for passing system arguments
from scipy.io.wavfile import read       # Scipy library for wave manipulation functions

def text_from_bits(bits, encoding='utf-8', errors='surrogatepass'):            # Function to convert a string of binary into a regular string
    n = int(bits, 2)
    return n.to_bytes((n.bit_length() + 7) // 8, 'big').decode(encoding, errors) or '\0'

def text_to_bits(text, encoding='utf-8', errors='surrogatepass'):              # Function to convert a string into a binary string
    bits = bin(int.from_bytes(text.encode(encoding, errors), 'big'))[2:]
    return bits.zfill(8 * ((len(bits) + 7) // 8))


def find_begining (begin_len, begin_str_bin, Queue, audio_data = []):          # Function to find the begining index of the message using an establish prefix
    compare_beg = [''] * (begin_len)
    start_index = 0
    while (list(begin_str_bin) != compare_beg):
        audio_data_bin = list (bin (audio_data [start_index, 0]))
        compare_beg = compare_beg [1 : begin_len]
        compare_beg.append(audio_data_bin [-1])
        start_index += 1
    Queue.put(start_index)

    
def find_end (end_len, end_str_bin, Queue, audio_data = []):                   # Function to find the end index of the message using an establish sufix
    end_index = 0
    compare_end = [''] * (end_len)
    while (list(end_str_bin) != compare_end):
        audio_data_bin = list (bin (audio_data [end_index, 0]))
        compare_end = compare_end [1 : end_len]
        compare_end.append(audio_data_bin [-1])
        end_index += 1
    Queue.put(end_index)
    
def decoder (myQueue, audio_data = []):                                        # Function to decode hiden message in LSB. Uses the previously found indexes to find the message
    hidden_message = ['']
    start_index = myQueue.get()                                                # Gets the variable from the queue established in a multiprocessing environment
    end_index = myQueue.get()
    for idx in range(start_index + 1, end_index - end_len):
        audio_data_bin = list (bin (audio_data [idx, 0])) 
        hidden_message.append(audio_data_bin [-1])             
    hidden_message_str = "".join(hidden_message)
    message = text_from_bits(hidden_message_str)
    print (message)


if __name__ == "__main__": # confirms that the code is under main function
    begin_str_bin = text_to_bits("**##**")                                     # Converts the prefix into binary string
    begin_len = len(begin_str_bin)                                             # Gets length of binary string
    end_str_bin = text_to_bits("##**##")
    end_len = len (end_str_bin)

    audio_in = sys.argv[1]                                              # Audio in argument, to be suplied at run time as an argument to the run file command

    file_data = read(audio_in)                                          # Scipy function to import audio as data
    audio_data = (file_data[1])                                         # The first colum gives the sample rate and this one gives the actual data array/list/matrix (whatever)
    
    myQueue = multiprocessing.Queue()
    thread1 = multiprocessing.Process(target=find_begining, args = (begin_len, begin_str_bin, myQueue, audio_data))
    thread2 = multiprocessing.Process(target=find_end, args = (end_len, end_str_bin, myQueue, audio_data))
    thread3 = multiprocessing.Process(target=decoder, args = (myQueue, audio_data))
    thread1.start()   
    thread2.start()
    thread3.start()
    thread1.join() 
    thread2.join() 
    thread3.join()

