import picamera as picam
from time import sleep

PATH = 'training_images/'
TIME_IN_HOURS = 4


camera = picam.PiCamera()
#images are 800 KiB
#if we take 2 pics per second, we can shoot 5 hours

time = TIME_IN_HOURS*3600
count = time*2
while count >=0:
    camera.capture(PATH+'pic_'+str(count)+'.jpg')
    sleep(0.5)
    count-=1
