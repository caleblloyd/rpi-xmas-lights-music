from config import is_rpi
import subprocess
import time
import pexpect


def player(mp3_file, interface, mp3_ready_event, gpio_queues, stop_events):
    process = ["omxplayer"]
    if interface:
        process.append("-o")
        process.append(interface)
    process.append('"'+mp3_file+'"')

    if is_rpi:
        p = pexpect.spawn(" ".join(process))
        p.expect(r'Audio')
        mp3_ready_event.set()
        p.wait()
    else:
        print process
        mp3_ready_event.set()
        time.sleep(10)

    for stop_event in stop_events:
        stop_event.set()
    if stop_events:
        print "song over, press any key to exit"

    for gpio_queue in gpio_queues:
        gpio_queue.put(-1)