import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(18, GPIO.OUT)
GPIO.output(18, GPIO.LOW)
led_state = False

pressed = False

#while not pressed:
#    pressed = GPIO.wait_for_edge(23, GPIO.RISING)
#print "Button pressed!"

prev_input = 0

while True:
    input = GPIO.input(17)
    if ((not prev_input) and input):
        print("Button Pressed")
	led_state = not led_state
	if led_state:
		GPIO.output(18,GPIO.HIGH)	
	else:
		GPIO.output(18,GPIO.LOW)
    prev_input = input
    time.sleep(0.05)


GPIO.cleanup()
