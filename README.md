# Overview
All of the arcade1up machines come with an on/off switch and a volume switch. I wanted to use these switches for what they were designed for but still be able to play games from a pi3. The solution was to hook the switches up to the GPIO pins on the pi3 and use a python script to turn the machine on/off and the volumne up/down.

In order to turn the machine on and off I used a wifi plug with support for IFTTT. I plugged in the monitor and amp into the plug. The pi I plugged in separately so it would remain on.

# Prerequisites
- [Raspberry pi3](https://www.amazon.com/Raspberry-Pi-RASPBERRYPI3-MODB-1GB-Model-Motherboard/dp/B01CD5VC92)
- [RetroPie](https://retropie.org.uk/)
- [Amp for volume](https://www.amazon.com/gp/product/B00OGZW54E)
- [Wifi plug that supports IFTTT](https://www.amazon.com/gp/product/B0786B1LGM)
Some way to connect the GPIO pins to the switches
- [GPIO pin connectors](https://www.amazon.com/Kuman-Breadboard-Arduino-Raspberry-Multicolored/dp/B01BV3Z342)
- [LED strip light cable](https://www.amazon.com/gp/product/B01E8RNLF6)
- Knowledge of hooking things up to GPIO pins and using python

# Connecting it up
I used the last 4 pins on the right side of the GPIO: Ground, 16, 20 and 21.
- Ground goes to the black wire on the power switch
- Ground goes to the middle wire on the volume switch (I used the same ground pin for both)
- 16 goes to the red wire on the power switch
- 20 goes to the left (volume lowest) pin of the volume switch
- 21 goes to the right (volume highest) pin of the volume switch

# Audio prerequisites
In order to adjust the volume you need to install alsaaudio

```sudo apt-get install python-alsaaudio```

# The scripts
There are three scripts provided:
1. on-off.py - This will turn your python on and off
2. volume.py - This will turn your volume up and down
3. on-off-and-volume.py - A combination of both
