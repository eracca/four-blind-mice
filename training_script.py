#!/usr/bin/python

#import picamera as picam
import pygame.camera
import RPi.GPIO as GPIO
from time import sleep
import os, sys

PATH = 'four-blind-mice/training_images/'
TIME_IN_MINUTES = 90

#setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.OUT) 
GPIO.output(18, GPIO.HIGH)
sleep(3)
GPIO.output(18, GPIO.LOW)

pressed = False
count = int(TIME_IN_MINUTES*60*2)
#camera = picam.PiCamera()
pygame.camera.init()
camera = pygame.camera.Camera(pygame.camera.list_cameras()[0], (1080, 1080))
camera.start()

#look for button press to start
while not pressed:
    try:
        pressed = GPIO.wait_for_edge(23, GPIO.RISING)
    except KeyboardInterrupt:
        break
pressed = True

print("Start recording")
for i in range(3):
    GPIO.output(18, GPIO.HIGH)
    sleep(1)
    GPIO.output(18, GPIO.LOW)
    sleep(1)

#record images
while count >=0:
    pressed = not GPIO.input(23)
    if not pressed:    
        print("Stopped recording")
        for i in range(2):
            GPIO.output(18, GPIO.HIGH)
            sleep(1)
            GPIO.output(18, GPIO.LOW)
            sleep(1)
        while not pressed:
            try:
                pressed = GPIO.wait_for_edge(23, GPIO.RISING)
            except KeyboardInterrupt:
                break
        print("Resumed recording")
        for i in range(3):
            GPIO.output(18, GPIO.HIGH)
            sleep(1)
            GPIO.output(18, GPIO.LOW)
            sleep(1)
    print("Recording")
    #camera.capture(PATH+ 'pic_'+str(count)+'.jpg')
    img = camera.get_image()
    pygame.image.save(img, PATH+ 'pic_' +str(count)+'.jpg')
    sleep(0.5)
    count-=1

print "Done recording"
GPIO.output(18, GPIO.HIGH)
pressed = False
while not pressed:
    try:
        pressed = GPIO.wait_for_edge(23, GPIO.RISING)
    except KeyboardInterrupt:
        break
GPIO.output(18, GPIO.HIGH)

GPIO.cleanup()
