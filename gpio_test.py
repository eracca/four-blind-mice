import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

pressed = False

#while not pressed:
#    pressed = GPIO.wait_for_edge(23, GPIO.RISING)
#print "Button pressed!"

prev_input = 0

while True:
    input = GPIO.input(23)
    if ((not prev_input) and input):
        print("Button Pressed")
    prev_input = input
    time.sleep(0.05)


GPIO.cleanup()
