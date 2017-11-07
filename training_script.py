import picamera as picam
import RPi.GPIO as GPIO
from time import sleep

PATH = 'training_images/'
TIME_IN_MINUTES = 1

#TODO: fix led issue

#setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.OUT) 
GPIO.output(18, GPIO.LOW)
pressed = False
count = TIME_IN_MINUTES*60*2
camera = picam.PiCamera()

#look for button press to start
while not pressed:
    pressed = GPIO.wait_for_edge(23, GPIO.RISING)
print "Begin recording"

#record iamges
while count >=0:
    camera.capture(PATH+ 'pic_'+str(count)+'.jpg')
    sleep(0.5)
    count-=1

print "Done recording"
GPIO.output(18, GPIO.HIGH)

GPIO.cleanup()
