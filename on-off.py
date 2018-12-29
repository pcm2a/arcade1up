import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import requests
from time import sleep

#
# This is the pin on the pi that you hook to the red wire
# on the on/off switch.
# Hook the black wire to ground on the pi.
#
ON_PIN = <The pin you hook to the red wire, example 16>

#
#
#
IFTTT_KEY = "<Place your key here, leave the quotes>"
IFTTT_ON_EVENT = "<Place your ON event name here, leave the quotes>"
IFTTT_OFF_EVENT = "<Place your OFF event name here, leave the quotes>"

#
# The amount of time to sleep between each check
# to see if the switch was changed
#
SLEEP_TIME = 1.0

#
# Since this is a switch and not a button we will record 
# the last state so we don't trigger the event over and over
#
onPushed = False

GPIO.setmode(GPIO.BCM)
GPIO.setup(ON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

def setPower():
	#print 'Power %s' % (onPushed)
	if onPushed:
		event = "https://maker.ifttt.com/trigger/%s/with/key/%s" % (IFTTT_ON_EVENT, IFTTT_KEY)
		r = requests.post(event)
		#print '%s, status=%s' % (r.text, r.status_code)
	else:
		event = "https://maker.ifttt.com/trigger/%s/with/key/%s" % (IFTTT_OFF_EVENT, IFTTT_KEY)
		r = requests.post(event)
		#print '%s, status=%s' % (r.text, r.status_code)

while True: # Run forever
	onStatus = GPIO.input(ON_PIN)
	if onStatus == GPIO.LOW and not onPushed: 
		onPushed = True	
		# turn on arcade
		setPower()
	elif onStatus == GPIO.HIGH and onPushed:
		onPushed = False
		# turn off arcade
		setPower()

	sleep(SLEEP_TIME)
