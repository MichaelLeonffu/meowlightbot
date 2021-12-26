# MeowLightBot
MeowLightBot

Night light Bot for Anna Li, runs on RPI0W. Requires a bit of setup outside of the bot's scope.

## Files

* cogs/...
* config/config.py:    Makes sure that the programs are configured with their settings
* meowlightbot.py:     Handles discord bot interfaces
* mainmeow.py:         Is run by crontab every 1 minute
* tools/gpio_debug.py: Useful to debugging gpio

## Usage

Meow Night Light comes with a button and a single blue LED as interface.

To make this more useful, a basic set of controls should be implemented on the single button:

* Single click
* Double click
* Triple click
* Long press
* Very long press and hold

The LED can:

* Turn on
* Turn off
* Blink X times

Finally Meow Night Light can be programmed or customized in the discord interface
i.e setting a on and off time for being used as night light; and setting the `single press`
option to toggle the state of the light at any time.

Note **The `very long press and hold` is reserved to resetting meowlightbot to factory settings.**

### Features

* As a night light
* Remembers your settings while in "offline" mode
* Petting your night light
* Showing the status of your night light on discord
* Having your own personal discord bot
* Sending you or your friend a "nya" when triple pressed
* Interactive blinking and pressing game

### Future concepts

* Blinking during certain channel notifications

## First time setup

For "online" features, including all discord features, meowlightbot must be configured to your wifi.

1. Connect the usb from meowlightbot into your computer.
2. Log into meowlightbot using a SSH terminal i.e putty or terminal; using the credentials included. e.g `ssh annali@meowbotpi.local`
3. Once in meowbotpi, configure the wifi settings by running the command `sudo raspi-config` followed by the password prompt.
System Options > Wireless LAN; then enter your SSID and passphrase for your wifi.
4. Once your meowbotpi is connected to the internet it should automatically come online within the minute!

*Disclaimer: meowbotpi may also perform self updates once connected to the internet.*

## Dev setup

If you want to work on meowlightbot then try the following setup. After installing the directory...

meowlightbot requires a discord api key but one should be included out of the box. If not then contact support.
Or make your own discord api key from discord developer portal; then place that into the config file. The config
file should be named `config.py` and be in the same shape as the template file.

### Venv

It's recommended to set up a venv using the command `python3 -m venv meowlightbot-venv` to create the venv dir.
Then running the command `source meowlightbot-venv/bin/activate` to activate the venv.

This keeps all your downloaded library files in the venv which makes it easier to develop and also remove.

For more information check out the [python venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) doc.

### Python

For python use [pip freeze](https://pip.pypa.io/en/stable/reference/pip_freeze/) to download all required libraries/packages

`pip3 install -r requirements.txt`

### Running

Running meowlightbot with a simple command:

`python3 -B meowlightbot.py`

## DevOps setup

In order to keep the program running and making sure permissions are set properly.

### Crontab

In order to make sure that **nya light** is working a program will run on boot and stay running.

It will use the crontab command to check every 1 minute:

	* * * * * ps aux | grep -v grep | grep -q mainmeow.py || python3 -B /home/annali/Developer/meowlightbot/meowlightbot/mainmeow.py &

The file will check if an instance of the program is already running, if it is running then
it won't boot another instance. I pulled the code from
[this stackoverflow](https://stackoverflow.com/questions/298760/how-to-make-sure-an-application-keeps-running-on-linux).

### Permissions

In order to use GPIO the user (which runs the program) needs to be given the GPIO group.

Running the command:

	sudo adduser annali gpio

Gives the user `annali` GPIO group. This should allow that user to run the program.

## References:

* [MichaelLeonffu/meowlightbot Github](https://github.com/MichaelLeonffu/meowlightbot)
* [Blinking LED Tutorial](https://raspberrypihq.com/making-a-led-blink-using-the-raspberry-pi-and-python/)
* [Pin Numbers](https://raspberrypihq.com/wp-content/uploads/2018/01/a-and-b-physical-pin-numbers.png)
* [Pinouts](https://pinout.xyz)
* [BC547B Transistor Doc](https://www.farnell.com/datasheets/410427.pdf)
* [Transistor Tutorial](https://www.dummies.com/article/technology/electronics/circuitry/electronics-components-use-a-transistor-as-a-switch-180034)
* [RPI GPIO python library tutorial](https://raspi.tv/2013/how-to-use-interrupts-with-python-on-the-raspberry-pi-and-rpi-gpio-part-2)
* [RPI GPIO python library docs](https://sourceforge.net/p/raspberry-gpio-python/wiki)


# WIP

## Maintenance/DevOps

To keep meowlightbot up-to-date is easy to do even from discord!

* `annali pull` Performs a git pull
* `annali reload` Reloads all cogs (do this after a pull)
* `annali close` Closes the annapythonli.py instance (run with marathon for automatic reboot)
* `annali xload` Runtime cog controler
* `annali free` Checks memeory on machine (only for linux)
* `annali press` Sets presence

### Development method

(Working on getting unit tests...) But for testing on the fly I do:
0. Change config to have differet bot prefix (`$`) and set `DEV_MODE=True`
1. Make change and save file
2. If it is not changing config/annapythonli.py then in discord type `&reload`
3. Test changes made

This is much faster than rebooting meowlightbot since reloading cogs takes very little effort
