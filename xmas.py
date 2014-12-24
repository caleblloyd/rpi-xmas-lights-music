import sys
import getopt
import os
import controller

def is_rpi():
    return os.uname()[4][:3] == 'arm'

class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg

def main(argv=None):
    if argv is None:
        argv = sys.argv
    try:
        try:
            opts, args = getopt.getopt(argv[1:], "h", ["help"])
        except getopt.error, msg:
             raise Usage(msg)


        """
        @todo
        1. Take a command line argument for a folder with an MP3 file in it
        2. Pass it to the controller
        """

        controller.start()



    except Usage, err:
        print >>sys.stderr, err.msg
        print >>sys.stderr, "for help use --help"
        return 2

if __name__ == "__main__":
    sys.exit(main())