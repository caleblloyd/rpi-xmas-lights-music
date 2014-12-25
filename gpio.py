from config import is_rpi

if is_rpi:
    import RPi.GPIO as gpio


def listener(relay_num, gpio_init, queue):
    if is_rpi:
        #init the gpio to gpio_init
        pass
    state = gpio_init
    while True:
        desired_state = queue.get()
        if desired_state not in [0, 1, 2]:
            break
        if desired_state == 2:
            desired_state = state ^ 1
        if desired_state != state:
            if is_rpi:
                #handle the pin state
                pass
            else:
                print "received", desired_state, "for", relay_num
            state = desired_state