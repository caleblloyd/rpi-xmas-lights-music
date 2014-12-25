from config import is_rpi
import time

def player(mp3_file, gpio_queues, keystroke_thread_stop):
    if is_rpi:
        #play the mp3
        pass
    else:
        print "playing",mp3_file
        time.sleep(10)

    keystroke_thread_stop.set()
    print "song over, press any key to exit"
    for gpio_queue in gpio_queues:
        gpio_queue.put(-1)