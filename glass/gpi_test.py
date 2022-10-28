import RPI.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(12, GPIO.IN, pull_up_down = GPIO.PUD.UP)

def myFunc(channel):
	print(f'{chnnel}pin pressed!')

GPIO.add_event_detect(12, GPIO.rising, callback=swotcjPressed)

try:
	while 1:
		print(".")
		time.sleep(0.1)

finally:
	gpio.cleanup()


