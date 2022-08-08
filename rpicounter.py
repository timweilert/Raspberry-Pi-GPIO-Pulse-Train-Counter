#!/usr/bin/env python3
import RPi.GPIO as GPIO
import threading
import time
input_gpio = 23

def count(self):
    global pulse_count
    global pulse_time
    if (pulse_time - time.time() > 0.2):
        pulse_count = 0
        pulse_count += 1
        pulse_time = time.time()

if __name__ == '__main__':
        global pulse_count
        global pulse_time
        pulse_count = 0
        pulse_time = time.time()
        input_gpio = 23

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(input_gpio, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
        GPIO.add_event_detect(input_gpio, GPIO.RISING, callback=count, bouncetime=90)

        while True:
                if (pulse_count != 0) & (time.time() - pulse_time > 0.5):
                        print(pulse_count)
                        pulse_count = 0

