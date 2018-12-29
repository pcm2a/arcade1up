import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import requests
import alsaaudio
from time import sleep

#
# This defines the pins that you hook to the left and right
# side of the switch. Hook the middle pin of the switch
# to ground on the pi.
#
VOL_LEFT_PIN = <The left pin of the volume switch, example 20>
VOL_RIGHT_PIN = <The right pin of the volumne switch, example 21>

#
# Set the volume levels for the left, middle and right switch
# positions. On my pi3 50% is too low so I used 90%.
#
VOLUME_OFF = 0
VOLUME_MID = 90
VOLUME_HIGH = 100

#
# Since this is a switch and not a button we will record
# the last state so we don't trigger the event over and over
#
volLeftPushed = False
volRightPushed = False

#
# If you encounter any problems try removing "PCM"
#
volume = alsaaudio.Mixer("PCM")
currentVolume = volume.getvolume()

GPIO.setmode(GPIO.BCM)
GPIO.setup(VOL_LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 
GPIO.setup(VOL_RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP) 

def setVolume(vol):
	global currentVolume
	#print 'Changing volume from %s to %s' % (currentVolume, vol)
	currentVolume = vol
	volume.setvolume(vol)

while True: # Run forever

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

	sleep(1.0)
