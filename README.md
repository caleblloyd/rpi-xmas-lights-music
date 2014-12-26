rpi-xmas-lights-music
=====================

Raspberry Pi sync christmas lights to music

1. Install linux dependencies pip and ffmpeg:
        
        sudo apt-get -y install python-setuptools
        sudo easy_install pip
        sudo apt-get -y install ffmpeg

2. Install python dependencies readchar, RPi.GPIO, pydub, and pexpect:

        sudo pip install readchar
        sudo pip install RPi.GPIO
        sudo pip install pydub
        sudo pip install pexpect
       
3. Program runs in 3 modes:

  - Record Mode

           sudo python xmas.py record /path/to/mp3_file.mp3
      
    Use keys defined in config.json to turn relays on/off/toggle.  Saves recording for future playback /path/to/mp3_file.xmas
    
  - Playback Mode
      
           sudo python xmas.py playback /path/to/mp3_file.mp3

    Plays back a sequence generated in record mode.  /path/to/mp3_file.xmas must exist.

  - Detect Mode

           sudo python xmas.py detect /path/to/mp3_file.mp3
      
    Uses FFT to detect frequency changes and automatically toggles relays
      

Configuration
===

Requires that you have a relay board.  Solid state relays are recommended.  Config file in "config.json" contains settings for:

  - num_relays: number of relays on your relay board
  - gpio_pins: pin numbers for gpio pins on the raspberry pi
  - gpio_init: initialization state for gpio pins at the beginning of the song
  - on_keys: keys that turn relays on in record mode
  - toggle_keys: keys that toggle relays in record mode
  - off_keys: keys that turn relays off in record mode
