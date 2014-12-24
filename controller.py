from threading import Thread
import keystrokes


def start():

    keystroke_thread = Thread(target=keystrokes.detect()).start()
    """
    1. Start the MP3 file in a thread
    2. Start the keystroke detection in a thread
    3. Use a queue to pass keystrokes to gpio threads
    """