# Simple program which should toggle the LED on button presses

import RPi.GPIO as GPIO # RPI GPIO library

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

# Pins settings
LED_PIN = 8
BUTTON_PIN = 10

# Set up the GPIO
# Set LED_PIN to be an output pin and set initial value to low (off)
# Set BUTTON_PIN to be an input pin and set it to low when its open circuit
GPIO.setup(LED_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Define the callback and the edge event detector for the button
def edge_detected_callback(channel):

    # Toggle LED
    GPIO.output(LED_PIN, not GPIO.input(LED_PIN))

# Tries for adding the event detect
# Sometimes adding the event detect fails and it's
# not really clear why it fails; this should retry to add the detect.
tries = 5

# On the rising and falling edge the callback function will be called
while tries > 0:
    try:
        GPIO.add_event_detect(BUTTON_PIN, GPIO.BOTH, callback=edge_detected_callback, bouncetime=300)
        # GPIO.add_event_detect(BUTTON_PIN, GPIO.FALLING, callback=falling_callback, bouncetime=200)
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
try:
    while True:
        pass

except KeyboardInterrupt:
    print("Test cancled, cleaning up GPIO.")
    GPIO.cleanup()

# Clean up
GPIO.cleanup()
