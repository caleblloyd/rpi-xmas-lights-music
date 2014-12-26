from datetime import datetime
import pickle
import time

def player(mp3_ready_event, gpio_queues, playback_file):

    record = pickle.load(open(playback_file, "r"))

    while not mp3_ready_event.is_set():
        time.sleep(.001)

    start = datetime.now()
    for line in record:
        while line[0] > (datetime.now() - start):
            time.sleep(.001)
        gpio_queues[line[1]].put(line[2])

