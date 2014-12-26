from config import config, is_rpi
import detect
import gpio
import mp3
import os
import playback
from Queue import Queue
import record
import signal
import sys
from threading import Thread, Event
import time

if is_rpi:
    import RPi.GPIO as GPIO


def start(mode, mp3_file, options):

    mp3_file = os.path.abspath(mp3_file)
    if not os.path.exists(mp3_file):
        raise Exception("File does not exist: " + mp3_file)

    if mode == 'record' or mode == 'playback':
        playback_file = os.path.splitext(mp3_file)[0] + ".xmas"

    if mode == 'playback':
        if not os.path.exists(playback_file):
            raise Exception("File does not exist: " + playback_file)

    if mode == 'detect':
        wav_fp, chunk_size, sample_rate = detect.setup_detection(mp3_file)

    if is_rpi:
        GPIO.setmode(GPIO.BOARD)

    sigint_event = Event()

    def signal_handler(signal, frame):
        print('Received SIGINT')
        sigint_event.set()

    signal.signal(signal.SIGINT, signal_handler)

    mp3_ready_event = Event()
    gpio_queues = [Queue() for _ in xrange(0, config['num_relays'])]
    stop_events = []
    threads = []

    if mode == 'record':
        keystroke_thread_stop = Event()
        stop_events.append(keystroke_thread_stop)
        record_thread = Thread(target=record.recorder, args=(mp3_ready_event, sigint_event, gpio_queues, keystroke_thread_stop, playback_file))
        record_thread.start()
        threads.append(record_thread)
    elif mode == 'playback':
        playback_thread = Thread(target=playback.player, args=(mp3_ready_event, sigint_event, gpio_queues, playback_file))
        playback_thread.start()
        threads.append(playback_thread)
    elif mode == 'detect':
        detect_thread = Thread(target=detect.detector, args=(mp3_ready_event, sigint_event, wav_fp, chunk_size, sample_rate, gpio_queues))
        detect_thread.start()
        threads.append(detect_thread)
    else:
        raise Exception("Invalid mode: " + mode)

    mp3_thread = Thread(target=mp3.player, args=(mp3_file, "local", mp3_ready_event, sigint_event, gpio_queues, stop_events))
    mp3_thread.start()
    threads.append(mp3_thread)

    for i in xrange(0, config['num_relays']):
        gpio_thread = Thread(target=gpio.listener, args=(i, config['gpio_pins'][i], config['gpio_init'][i], gpio_queues[i]))
        gpio_thread.start()
        threads.append(gpio_thread)

    while True:
        threads_done = True
        for t in threads:
            if t.isAlive():
                threads_done = False

        if threads_done:
            break

        time.sleep(0.1)