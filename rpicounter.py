#!/usr/bin/env python3

import RPi.GPIO as GPIO
import threading
import time
import subprocess

input_gpio = 26
hook_gpio = 16

def hook(self):
	global hook_gpio
	global dial_list
	global previous_pin_status
	global dial_tone_process
	print("Hook")
	pin_status = GPIO.input(hook_gpio)
	print(pin_status)
	if pin_status == 0: #reciever off the hook
		if previous_pin_status == 1: 
			dial_list.clear()
			print("you picked up")
			dial_tone_process = subprocess.Popen("mplayer ./dial_tone.mp3", shell = True)
	if pin_status == 1: #receiver is hung up
		dial_list.clear()
		if previous_pin_status == 0:
			print("you hung up")
			subprocess.Popen("killall -9 mplayer", shell = True)
	previous_pin_status = pin_status

def count(self):
	global pulse_count
	global pulse_time
	if (pulse_time - time.time() > 0.2):
		 pulse_count = 0
	pulse_count += 1
	pulse_time = time.time()

def listToString(list):
	emptystr=""
	for element in list:
		emptystr += element
	return emptystr

if __name__ == '__main__':

	global pulse_count
	global pulse_time
	global previous_pin_status
	global dial_list

	dial_list = []
	pulse_count = 0
	pulse_time = time.time()
	previous_pin_status = 1

	GPIO.setmode(GPIO.BCM)
	GPIO.setup(input_gpio, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.setup(hook_gpio, GPIO.IN, pull_up_down = GPIO.PUD_UP)
	GPIO.add_event_detect(input_gpio, GPIO.RISING, callback=count, bouncetime=90)
	GPIO.add_event_detect(hook_gpio, GPIO.BOTH, callback=hook, bouncetime=90)

	hook('self')
	while True:
		if (pulse_count != 0) & ((time.time() - pulse_time) > 0.5) & (previous_pin_status == 0):
			print("Rotary Count")
			print(pulse_count)
			if pulse_count == 10:
				pulse_count = 0
			dial_list.append(str(pulse_count))
			print(dial_list)
			pulse_count = 0
			if len(dial_list) == 5:
				zip = listToString(dial_list)
				print(zip)
				dial_list = []
				subprocess.Popen("killall -9 mplayer", shell = True)
				command_string = "ruby /home/dlynch/automatic-david-lynch-weather/weather.rb %s" % (zip)
				subprocess.Popen(command_string, shell = True)
