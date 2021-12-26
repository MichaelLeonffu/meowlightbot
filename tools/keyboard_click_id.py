# !!! This is the same as `gpio_click_id.py` except this uses keyboard clicks
# To check for the logic without the need of a physical button.
# The difference is that the mainloop will be checking for input.
# This uses the "pynput" module which has to be installed.

# This program should blink the LED until the button is pressed

import time
import datetime
import threading
from pynput import keyboard

# Keybarod settings
KEYBOARD_KEY = 'a'

# Times in ms
CLICK_TIMEOUT_TIME = 1000
LONG_PRESS_TIME = 2000
VERY_LONG_PRESS_TIME = 9000

# Global vars
main_loop = True

# Datetime for delta time
start_time = datetime.datetime.now()

# Counts the number of clicks that are ongoing.
click_counter = 0

# Once the click count is known, process it; print it out to screen
def process_click(click_count):
    print("Click processed: ", click_count)

# Processing longer clicks
def process_long_click():
    print("Long Click processed")

def process_very_long_click():
    global main_loop
    print("Very Long Click processed")
    main_loop = False

# Times out the click if it takes too long, track which click it's on as well
# This function should return a function with a fixed value for it's click_count
def click_timeout(click_count):
    global click_counter

    # This is a local copy of the CURRENT value of the click_count
    # click_count

    # When the click times out, it'll check if the click_count = the current value
    def click_timmed_out():
        global click_counter
        if click_counter > click_count:
            # Do nothing, a new click was clicked
            pass
        else:
            # There is no new click then this is the final click count
            click_counter = 0
            process_click(click_count)

    return click_timmed_out



# Define the callback and the edge event detector for the button
def edge_detected_callback(updown):
    global start_time
    global click_counter

    # Check if rising edge or falling edge
    
    # High --> rising edge
    if updown:

        # Record the time of the rising edge
        start_time = datetime.datetime.now()

    # Low --> Falling edge
    else:
        # Find the delta time for the length of the click
        delta = datetime.datetime.now() - start_time
        deltams = int(delta.total_seconds() * 1000)

        # If time difference is less than small hold time then it's a click
        if deltams < LONG_PRESS_TIME:
            # Click, increment the click counter
            click_counter += 1

            # Start the timmer to timeout the click counter
            start_time = threading.Timer(CLICK_TIMEOUT_TIME/1000, click_timeout(click_counter))
            start_time.start()

        # If time difference is less than long hold time then it's a long press
        elif deltams < VERY_LONG_PRESS_TIME:
            # Long press, reset click counter and execute long press function
            click_counter = 0
            process_long_click()

        # Otherwise it is the longest press
        else:
            # Very long press, reset click counter and execute very long press function
            click_counter = 0
            process_very_long_click()


# Can only press if released
pressed = False

# Create event listeners for the key presses
def on_press(key):
    global pressed
    try:
        if key.char == KEYBOARD_KEY:
            if pressed:
                return
            pressed = True
            edge_detected_callback(True)
            return
        print('Alphanumeric key pressed: {0} '.format(key.char))
    except AttributeError:
        print('special key pressed: {0}'.format(key))

def on_release(key):
    global pressed
    try:
        if key.char == KEYBOARD_KEY:
            if not pressed:
                return
            pressed = False
            edge_detected_callback(False)
            return
        print('Key released: {0}'.format(key))
        if key == keyboard.Key.esc:
            # Stop listener
            return False
    except AttributeError:
        print('special key pressed: {0}'.format(key))

# Test
print("Starting test, until program stops i.e 10s press.")
try:
    # Collect events until released
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener: listener.join()

except KeyboardInterrupt:
    print("Test cancled.")


