from config import is_rpi
import time
import pexpect


def player(mp3_file, interface, mp3_ready_event, sigint_event, gpio_queues, stop_events):
    process = ["omxplayer"]
    if interface:
        process.append("-o")
        process.append(interface)
    process.append('"'+mp3_file+'"')

    if is_rpi:
        p = pexpect.spawn(" ".join(process))
        p.expect(r'Audio')
    else:
        p = pexpect.spawn("sleep 10")

    mp3_ready_event.set()
    while p.isalive():
        if sigint_event.is_set():
            p.terminate()
        else:
            time.sleep(1)

    for stop_event in stop_events:
        stop_event.set()
    if stop_events:
        print "song over, press any key to exit"

    for gpio_queue in gpio_queues:
        gpio_queue.put(-1)