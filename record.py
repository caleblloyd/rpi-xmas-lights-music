import readchar
from config import config
from datetime import datetime
import pickle

def recorder(gpio_queues, thread_stop, playback_file):
    start = datetime.now()
    record = []

    while not thread_stop.is_set():
        c = readchar.readchar()
        desired_state = -1
        index = 0
        if c in config['on_keys']:
            index = config['on_keys'].index(c)
            desired_state = 1
        if c in config['off_keys']:
            index = config['off_keys'].index(c)
            desired_state = 0
        if c in config['toggle_keys']:
            index = config['toggle_keys'].index(c)
            desired_state = 2

        if desired_state >= 0:
            gpio_queues[index].put(desired_state)
            record.append(((datetime.now()-start), index, desired_state))

    pickle.dump(record, open(playback_file, "wb"))