import RPi.GPIO as GPIO

pin_lights = 32

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(pin_lights, GPIO.OUT)
pwm_led = GPIO.PWM(pin_lights, 500) # PIN_CameraPitch = GPIO pin 38, frequency 200
pwm_led.start(0)

pwm_led.ChangeDutyCycle(50)
while True:
    pass