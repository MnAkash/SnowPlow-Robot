import RPi.GPIO as GPIO          

import time

class motorControl:
    def __init__(self):

        self.dir1 = 16
        self.dir2 = 22
        self.pwm1 = 18
        self.pwm2 = 19


        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pwm1,GPIO.OUT)
        GPIO.setup(self.pwm2,GPIO.OUT)
        GPIO.setup(self.dir1,GPIO.OUT)
        GPIO.setup(self.dir2,GPIO.OUT)

        GPIO.output(self.dir1,GPIO.HIGH)
        GPIO.output(self.dir2,GPIO.HIGH)

        self.motor1=GPIO.PWM(self.pwm1,1000)
        self.motor2=GPIO.PWM(self.pwm2,1000)

        self.motor1.start(0)
        self.motor2.start(0)

    def backward(self, speed):
        #speed in percentage
        GPIO.output(self.dir1,GPIO.HIGH) #motor1 forward direction
        GPIO.output(self.dir2,GPIO.HIGH) #motor2 forward direction

        self.motor1.ChangeDutyCycle(speed)
        self.motor2.ChangeDutyCycle(speed)

    def forward(self, speed):
        GPIO.output(self.dir1,GPIO.LOW) #motor1 forward direction
        GPIO.output(self.dir2,GPIO.LOW) #motor2 forward direction

        self.motor1.ChangeDutyCycle(speed)
        self.motor2.ChangeDutyCycle(speed)

    def right(self, speed):
        GPIO.output(self.dir1,GPIO.LOW) #motor1 backward direction
        GPIO.output(self.dir2,GPIO.HIGH) #motor2 forward direction

        self.motor1.ChangeDutyCycle(speed)
        self.motor2.ChangeDutyCycle(speed)

    def left(self, speed):
        GPIO.output(self.dir1,GPIO.HIGH) #motor1 forward direction
        GPIO.output(self.dir2,GPIO.LOW) #motor2 backward direction

        self.motor1.ChangeDutyCycle(speed)
        self.motor2.ChangeDutyCycle(speed)

    def brake(self):
        self.motor1.ChangeDutyCycle(0)
        self.motor2.ChangeDutyCycle(0)
