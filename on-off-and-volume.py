import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import requests
import alsaaudio
from time import sleep

#
# This is the pin on the pi that you hook to the red wire
# on the on/off switch.
# Hook the black wire to ground on the pi.
#
ON_PIN = <The pin you hook to the red wire, example 16>

#
# This defines the pins that you hook to the left and right
# side of the switch. Hook the middle pin of the switch
# to ground on the pi.
#
VOL_LEFT_PIN = <The left pin of the volume switch, example 20>
VOL_RIGHT_PIN = <The right pin of the volumne switch, example 21>

#
#
#
IFTTT_KEY = "<Place your key here, leave the quotes>"
IFTTT_ON_EVENT = "<Place your ON event name here, leave the quotes>"
IFTTT_OFF_EVENT = "<Place your OFF event name here, leave the quotes>"

#
# Set the volume levels for the left, middle and right switch
# positions. On my pi3 50% is too low so I used 90%.
#
VOLUME_OFF = 0
VOLUME_MID = 90
VOLUME_HIGH = 100

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
volLeftPushed = False
volRightPushed = False

#
# If you encounter any problems try removing "PCM"
#
volume = alsaaudio.Mixer("PCM")
currentVolume = volume.getvolume()

GPIO.setmode(GPIO.BCM)
GPIO.setup(ON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(VOL_LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(VOL_RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

def setVolume(vol):
	global currentVolume
	#print 'Changing volume from %s to %s' % (currentVolume, vol)
	currentVolume = vol
	volume.setvolume(vol)

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

	leftStatus = GPIO.input(VOL_LEFT_PIN)
	if leftStatus == GPIO.LOW and not volLeftPushed:
		volLeftPushed = True
		# mute volume
		setVolume(VOLUME_OFF)
	elif leftStatus == GPIO.HIGH and volLeftPushed:
		volLeftPushed = False

	rightStatus = GPIO.input(VOL_RIGHT_PIN)
	if rightStatus == GPIO.LOW and not volRightPushed:
		volRightPushed = True
		# max volume
		setVolume(VOLUME_HIGH)
	elif rightStatus == GPIO.HIGH and volRightPushed:
		volRightPushed = False

	if not volLeftPushed and not volRightPushed and currentVolume != 50:
		# set volume to 50
		setVolume(VOLUME_MID)

	sleep(SLEEP_TIME)
