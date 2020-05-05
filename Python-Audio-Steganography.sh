#!/bin/sh

# This is a shell script that runs two other python3 scripts (encoder.py and decoder.py) in order to use audio Steganography [https://en.wikipedia.org/wiki/Steganography] to conceal a text message to be introduced by the user.
#This script requires and additional audio file in ".wav" extension and encoding to be provided so as to hide said message. 

clear; 	# clears console

set -u		# treat undefined variables as errors

STOP () { 	# function to stop script in case of error
        echo "ERROR: Only one choice allowed! [-e] or [-d]" 
        exit 1
}

while getopts ':e:d:' opt;do  case ${opt} in
    e)			# encoding option
    	[ $# -gt 2 ] && STOP	# if #arguments is greater than 2 STOP this script    	
    	read -p "Insert message to hide: " message
	python3 encoder.py "$message" $OPTARG coded_audio.wav
      	;;
    d)			# Decoding option
    	[ $# -gt 2 ] && STOP	# if #arguments is greater than 2 STOP this script  
	echo "decoded message is:";
      	python3 decoder.py $OPTARG
      	;;
    :)			# when no argument is added
	echo "option -$OPTARG needs an input file <filename.wav>"
	;;
    *)			# for all other possible choices present error
      	echo "script usage: $(basename $0) [-e] or [-d] <filename.wav>" >&2
      	exit 1
      	;;
  esac
done

[ $OPTIND -eq 1 ] && echo -e "No option was chosen. \nscript usage: $(basename $0) [-e] or [-d] [filename] \n[-e] for encoding audio + <filename.wav> \n[-d] for decoding audio + <filename.wav>"

shift "$(($OPTIND -1))" # remove  options
