from config import config, is_rpi
import gpio
import mp3
import os
import playback
from Queue import Queue
import record
from threading import Thread, Event

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

    if is_rpi:
        GPIO.setmode(GPIO.BOARD)

    gpio_queues = [Queue() for _ in xrange(0, config['num_relays'])]
    stop_events = []

    if mode == 'record':
        keystroke_thread_stop = Event()
        stop_events.append(keystroke_thread_stop)
        Thread(target=record.recorder, args=(gpio_queues, keystroke_thread_stop, playback_file)).start()
    elif mode == 'playback':
        Thread(target=playback.player, args=(gpio_queues, playback_file)).start()
        pass

    Thread(target=mp3.player, args=(mp3_file, "local", gpio_queues, stop_events)).start()

    for i in xrange(0, config['num_relays']):
        Thread(target=gpio.listener, args=(i, config['gpio_pins'][i], config['gpio_init'][i], gpio_queues[i])).start()