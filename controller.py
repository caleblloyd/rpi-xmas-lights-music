from config import config
import gpio
import keystrokes
import mp3
from Queue import Queue
from threading import Thread, Event

def start(mp3_file):

    keystroke_thread_stop = Event()
    gpio_queues = [Queue() for _ in xrange(0, config['num_relays'])]

    mp3_thread = Thread(target=mp3.player, args=(mp3_file, gpio_queues, keystroke_thread_stop)).start()
    keystroke_thread = Thread(target=keystrokes.listener, args=(gpio_queues, keystroke_thread_stop)).start()
    gpio_threads = [Thread(target=gpio.listener, args=(i, config['gpio_init'][i], gpio_queues[i])).start() for i in xrange(0, config['num_relays'])]