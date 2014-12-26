import json
import os

json_data = open(os.path.dirname(os.path.realpath(__file__)) + os.path.sep + 'config.json')
config = json.load(json_data)
json_data.close()

is_rpi = os.uname()[4][:3] == 'arm'