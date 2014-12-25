import sys
import getopt
import os
import controller

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hlh", ["help", "local", "hdmi"])
        except getopt.error, msg:
             raise Usage(msg)


        """
        @todo
        1. Take a command line argument for a MP3 file
        2. Pass it to the controller
        """

        if len(args) < 2:
            raise Usage("xmas.py [-o local|hdmi] record|playback|detect mp3_file")

        controller.start(args[0], args[1], opts)


    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())