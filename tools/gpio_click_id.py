# This program should blink the LED until the button is pressed

import RPi.GPIO as GPIO # RPI GPIO library
import time
import datetime
import threading

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

# Pins settings
led_pin = 8
button_pin = 10

# Times in ms
CLICK_TIMEOUT_TIME = 1000
LONG_PRESS_TIME = 2000
VERY_LONG_PRESS_TIME = 9000

# Set up the GPIO
# Set led_pin to be an output pin and set initial value to low (off)
# Set button_pin to be an input pin and set it to low when its open circuit
GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

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
def edge_detected_callback(channel):
    global start_time
    global click_counter

    # Check if rising edge or falling edge
    
    # High --> rising edge
    if GPIO.input(channel):

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


# Tries for adding the event detect
# Sometimes adding the event detect fails and it's
# not really clear why it fails; this should retry to add the detect.
tries = 5

# On the rising and falling edge the callback function will be called
while tries > 0:
    try:
        GPIO.add_event_detect(button_pin, GPIO.BOTH, callback=edge_detected_callback, bouncetime=200)
        # GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=falling_callback, bouncetime=200)
        break
    except RuntimeError as e:
        print("RuntimeError", e)
        print("Likely failed due to some other secondary use of the pins.")
        print("Should try again until it doesn't fail for up to ({}) tries.".format(tries))
        tries -= 1

# If tries are run out then just fail
if tries == 0:
    print("Failed too many times, exit program.")
    GPIO.cleanup()
    exit()

# Test
print("Starting test, blink LED until program stops i.e 10s press.")
try:
    while main_loop:
        pass

except KeyboardInterrupt:
    print("Test cancled, cleaning up GPIO.")
    GPIO.cleanup()

# Clean up
GPIO.cleanup()
