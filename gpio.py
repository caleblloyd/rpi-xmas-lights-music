from config import is_rpi

if is_rpi:
    import RPi.GPIO as GPIO


def set_gpio_state(gpio_pin, state):
    if state:
        GPIO.output(gpio_pin, GPIO.HIGH)
    else:
        GPIO.output(gpio_pin, GPIO.LOW)


def listener(relay_num, gpio_pin, gpio_init, queue):
    state = gpio_init

    if is_rpi:
        GPIO.setup(gpio_pin, GPIO.OUT)
        set_gpio_state(gpio_pin, state)

    while True:
        desired_state = queue.get()
        if desired_state not in [0, 1, 2]:
            break
        if desired_state == 2:
            desired_state = state ^ 1
        if desired_state != state:
            if is_rpi:
                set_gpio_state(gpio_pin, desired_state)
                print "received", desired_state, "for", relay_num
            else:
                print "received", desired_state, "for", relay_num
            state = desired_state

    if is_rpi:
        state = gpio_init
        set_gpio_state(gpio_pin, state)