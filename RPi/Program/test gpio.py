import RPi.GPIO as GPIO

pin_lights = 12

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(pin_lights, GPIO.OUT)
pwm_led = GPIO.PWM(pin_lights, 50) # PIN_CameraPitch = GPIO pin 38, frequency 200
pwm_led.start(10)


while True:
    pwm_led.ChangeDutyCycle(7)
    print("ok")