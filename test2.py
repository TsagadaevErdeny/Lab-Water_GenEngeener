import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(15, GPIO.IN)
while True:
    start_time = time.time()
    while not GPIO.input(15):
        exp_time = time.time() - start_time
        print("Эксперимент идет! Время: ", exp_time)
    time.sleep(1)