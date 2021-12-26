# From https://raspberrypihq.com/making-a-led-blink-using-the-raspberry-pi-and-python/

# This program should blink the LED until the button is pressed

import RPi.GPIO as GPIO # RPI GPIO library
import time

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BOARD) # Use physical pin numbering

# Pins settings
led_pin = 8
button_pin = 10

# Set up the GPIO
# Set led_pin to be an output pin and set initial value to low (off)
# Set button_pin to be an input pin and set it to low when its open circuit
GPIO.setup(led_pin, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Global, should be set to True after button is pressed
button_pressed = False

# Define the callback and the event detector for the button
def my_callback(channel):
    global button_pressed
    print("falling edge detected from button")
    button_pressed = True

# Tries for adding the event detect
# Sometimes adding the event detect fails and it's
# not really clear why it fails; this should retry to add the detect.
tries = 5

# On the falling edge the callback function will be called
while tries > 0:
    try:
        GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=my_callback, bouncetime=300)
        break
    except RuntimeError as e:
        print("RuntimeError", e)
        print("Likely failed due to some other secondary use of the pins.")
        print("Should try again until it doesn't fail for up to ({}) tries.".format(tries))


# Test
print("Starting test, blink LED until button is pressed.")
try:
    while not button_pressed:

        # Blink led at 250ms until
        GPIO.output(led_pin, GPIO.HIGH)
        time.sleep(250 / 1000)
        GPIO.output(led_pin, GPIO.LOW)
        time.sleep(250 / 1000)

except KeyboardInterrupt:
    print("Test cancled, cleaning up GPIO.")
    GPIO.cleanup()

# Clean up
GPIO.cleanup()
