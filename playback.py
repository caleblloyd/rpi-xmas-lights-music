from datetime import datetime
import pickle
import time

def player(mp3_ready_event, sigint_event, gpio_queues, playback_file):

    record = pickle.load(open(playback_file, "r"))

    while not mp3_ready_event.is_set() and not sigint_event.is_set():
        time.sleep(.001)

    start = datetime.now()
    for line in record:
        while line[0] > (datetime.now() - start) and not sigint_event.is_set():
            time.sleep(.001)
        if sigint_event.is_set():
            break
        gpio_queues[line[1]].put(line[2])

