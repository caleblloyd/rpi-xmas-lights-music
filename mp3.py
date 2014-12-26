from config import is_rpi
import subprocess
import time

def player(mp3_file, interface, gpio_queues, stop_events):

    process = ["omxplayer"]
    if interface:
        process.append("-o")
        process.append("local")
    process.append(mp3_file)

    if is_rpi:
        p = subprocess.Popen(process)
        p.wait()
    else:
        print process
        time.sleep(10)

    for stop_event in stop_events:
        stop_event.set()
    if stop_events:
        print "song over, press any key to exit"

    for gpio_queue in gpio_queues:
        gpio_queue.put(-1)