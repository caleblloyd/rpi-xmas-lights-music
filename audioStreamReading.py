#!/usr/bin/env python

# 8 bar Audio equaliser using MCP2307
 
import alsaaudio as aa
import audioop
import smbus
import sys
from time import sleep
import numpy as np
from pydub import AudioSegment
from struct import unpack
import wave
import subprocess
import os.path

if not (os.path.isfile(sys.argv[1]+"output/"+sys.argv[2]+".wav")):
    sound = AudioSegment.from_mp3(sys.argv[1]+sys.argv[2]+".mp3")
    sound.export(sys.argv[1]+"output/"+sys.argv[2]+".wav", format="wav")


def calculate_levels(data, chunk, sample_rate):
   # Convert raw data to numpy array
   data = unpack("%dh"%(len(data)/2),data)
   data = np.array(data, dtype='h')
   # Apply FFT - real data so rfft used
   fourier=np.fft.rfft(data)
   # Remove last element in array to make it the same size as chunk
   fourier=np.delete(fourier,len(fourier)-1)
   # Find amplitude
   if not 0 in fourier:
       power = np.log10(np.abs(fourier))**2

       # Araange array into 8 rows for the 8 bars on LED matrix
       power = np.reshape(power,(4,chunk/4))
       matrix= np.int_(np.average(power,axis=1)/4)

       return matrix
   return [0,0,0,0]
# Initialise matrix
#TurnOffLEDS()
matrix=[0,0,0,0]

# Set up audio
wavfile = wave.open(sys.argv[1]+"output/"+sys.argv[2]+'.wav','r')
sample_rate = wavfile.getframerate()
no_channels = wavfile.getnchannels()
chunk = 1024
output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL)
output.setchannels(no_channels)
output.setrate(sample_rate)
output.setformat(aa.PCM_FORMAT_S16_LE)
output.setperiodsize(chunk)

subprocess.call(["omxplayer","-o","local","~/frozen-let-it-go.mp3"]);

print "Processing....."

os.system("")
data = wavfile.readframes(chunk)
while data!='':
   output.write(data)

   matrix = calculate_levels(data,chunk,sample_rate)
   for i in range(0,4):
       if matrix[i] <= 2:
           matrix[i] = 0
       else:
           matrix[i] = 1
   print matrix

   data = wavfile.readframes(chunk)
   #TurnOffLEDS()