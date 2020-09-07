import RPi.GPIO as GPIO
import time,random
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(21,GPIO.OUT)#high

tmp=100
value=0
#temp=int(input())
def rand():
    return random.randint(50,75)
def rand1():
    return random.randint(10,20)
    
if GPIO.output(21,1):
    temp=2

if GPIO.output(21,0):
    temp=1


if temp==2:
    value=rand()
if temp==1:
    value=rand1()
print (value)
