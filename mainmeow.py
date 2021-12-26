# This is the main running program that will be spawned back
# via crontab. It will be the entry point to the whole software.

import config.config as config
import json
import os
import time

### PREFERENCES:

if not os.path.exists(config.PREFERENCES_PATH):
    # Generate new `preferences.json`
    print(time.ctime(), "No Prefereneces file detected. Generating preferences file.")

    # serializing json
    preferences_json = json.dumps(config.PREFERENCES_DEFAULTS, indent = 4)
      
    # Writing to preferences path
    with open(config.PREFERENCES_PATH, "w") as preferences_file:
        preferences_file.write(preferences_json)

# Opening `prefernces.json` file
with open(config.PREFERENCES_PATH, 'r') as preferences_file:
    preferences = json.load(preferences_file)


### Something else


### Something else


