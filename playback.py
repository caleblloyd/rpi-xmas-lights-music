from datetime import datetime
import pickle
import time

def player(gpio_queues, playback_file):
    start = datetime.now()
    record = pickle.load(open(playback_file, "r"))

    for line in record:
        while line[0] > (datetime.now() - start):
            time.sleep(.001)
        gpio_queues[line[1]].put(line[2])

