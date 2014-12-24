import readchar

def detect():
    while True:
        c = readchar.readchar()
        if str(c) == 'q':
            break
        else:
            print repr(c)