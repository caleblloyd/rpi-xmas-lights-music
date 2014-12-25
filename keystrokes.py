import readchar
from config import config

def listener(gpio_queues, thread_stop):
    while not thread_stop.is_set():
        c = readchar.readchar()
        if c in config['on_keys']:
            index = config['on_keys'].index(c)
            gpio_queues[index].put(1)
        if c in config['off_keys']:
            index = config['off_keys'].index(c)
            gpio_queues[index].put(0)
        if c in config['toggle_keys']:
            index = config['toggle_keys'].index(c)
            gpio_queues[index].put(2)