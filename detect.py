#!/usr/bin/env python

# 8 bar Audio equaliser using MCP2307

# import alsaaudio as aa
import sys
from config import config, is_rpi
import collections
import numpy as np
from pydub import AudioSegment
from struct import unpack
import wave
# import subprocess
import os.path
from datetime import datetime, timedelta
import time


def setup_detection(mp3_file):
    wav_file = os.path.splitext(mp3_file)[0] + ".wav"

    if not os.path.exists(wav_file):
        sound = AudioSegment.from_mp3(mp3_file)
        sound.export(wav_file, format="wav")

    wav_fp = wave.open(wav_file, 'r')
    sample_rate = wav_fp.getframerate()
    chunk_size = 4096
    return wav_fp, chunk_size, sample_rate


    # Set up audio

    # no_channels = wav_fp.getnchannels()

    # output = aa.PCM(aa.PCM_PLAYBACK, aa.PCM_NORMAL)
    # output.setchannels(no_channels)
    # output.setrate(sample_rate)
    # output.setformat(aa.PCM_FORMAT_S16_LE)
    # output.setperiodsize(chunk)




def calculate_levels(data, chunk, sample_rate):
    # Convert raw data to numpy array
    data = unpack("%dh" % (len(data) / 2), data)
    data = np.array(data, dtype='h')
    # Apply FFT - real data so rfft used
    fourier = np.fft.rfft(data)
    # Remove last element in array to make it the same size as chunk
    fourier = np.delete(fourier, len(fourier) - 1)
    # Find amplitude
    if not 0 in fourier:
        power = np.log10(np.abs(fourier)) ** 2

        # Araange array into 8 rows for the 8 bars on LED matrix
        power = np.reshape(power, (4, chunk / 4))
        matrix = np.int_(np.average(power, axis=1) / 4)

        return matrix
    return [0, 0, 0, 0]


def detector(mp3_ready_event, sigint_event, wav_fp, chunk_size, sample_rate, gpio_queues):
    print "Detecting..."

    chunk_time = 1. / sample_rate * chunk_size
    chunk_no = 0
    threshold_off_min = [2.5, 1.5, 1.5, 2.5]
    threshold_seed = [3, 2, 2, 3]
    threshold_size = 30
    threshold_deque = [collections.deque() for _ in xrange(0, config['num_relays'])]
    for i,d in enumerate(threshold_deque):
        for _ in xrange(threshold_size):
            d.append(threshold_seed[i])


    data = wav_fp.readframes(chunk_size)

    while not mp3_ready_event.is_set():
        time.sleep(.001)

    start = datetime.now()

    while data and not sigint_event.is_set():
        frame_time_secs = chunk_time * chunk_no
        frame_time_delta = timedelta(seconds=frame_time_secs)
        frame_time_plus_one_secs = frame_time_secs + chunk_time
        frame_time_plus_one_delta = timedelta(seconds=frame_time_plus_one_secs)

        while frame_time_delta > (datetime.now() - start):
            time.sleep(.0001)

        # only process frame if we're not too far behind
        if frame_time_plus_one_delta > (datetime.now() - start):

            # output.write(data)
            matrix = calculate_levels(data, chunk_size, sample_rate)
            # print matrix

            for i in range(0, config['num_relays']):
                d = threshold_deque[i]
                threshold = reduce(lambda x, y: float(x) + float(y), d) / len(d)

                d.append(matrix[i])
                if len(d) > threshold_size:
                    d.popleft()

                if matrix[i] > max(threshold, threshold_off_min[i]):
                    matrix[i] = 1
                else:
                    matrix[i] = 0
            # print matrix

            for i,v in enumerate(matrix):
                gpio_queues[i].put(v)

        if not is_rpi and (datetime.now() - start).seconds > 10:
            break

        chunk_no += 1
        data = wav_fp.readframes(chunk_size)

    wav_fp.close()