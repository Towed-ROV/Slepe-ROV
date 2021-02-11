import RPi.GPIO as GPIO
import time

class Lights:
    def __init__(self):
        self.pin_led_lights = 13
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.pin_led_lights, GPIO.OUT)


    def set_lights(self, on_off):
        GPIO.output(self.pin_led_lights, on_off)
