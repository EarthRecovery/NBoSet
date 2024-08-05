import RPi.GPIO as GPIO

import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(8,GPIO.IN)

while True:
    print(f"{GPIO.input(8)}\n")
    time.sleep(0.1)

GPIO.cleanup()