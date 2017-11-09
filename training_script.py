#!/usr/bin/python

import picamera as picam
import RPi.GPIO as GPIO
from time import sleep

PATH = 'four-blind-mice/training_images/'
TIME_IN_MINUTES = 0.5

#setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.OUT) 
GPIO.output(18, GPIO.HIGH)
sleep(3)
GPIO.output(18, GPIO.LOW)

pressed = False
count = int(TIME_IN_MINUTES*60*2)
camera = picam.PiCamera()

#look for button press to start
while not pressed:
    try:
        pressed = GPIO.wait_for_edge(23, GPIO.RISING)
    except KeyboardInterrupt:
        break

print("Start recording")
for i in range(3):
    GPIO.output(18, GPIO.HIGH)
    sleep(1)
    GPIO.output(18, GPIO.LOW)
    sleep(1)

#record images
while count >=0:
    camera.capture(PATH+ 'pic_'+str(count)+'.jpg')
    sleep(0.5)
    count-=1

print "Done recording"
GPIO.output(18, GPIO.HIGH)
sleep(5)

GPIO.cleanup()
