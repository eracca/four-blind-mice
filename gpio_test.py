import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

pressed = False

while not pressed:
    pressed = GPIO.wait_for_edge(23, GPIO.RISING)
print "Button pressed!"

GPIO.cleanup()
