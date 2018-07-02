#!/usr/bin/python
# Head Control

import time
from Tkinter import *
import RPi.GPIO as GPIO
import socket
#import chat
import threading
import multiprocessing as mp
import config as conf


# Get Pi's IP Address and Print it to terminal
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP
print('Enter this IP address on client side to access server: \n' + get_ip())

# Start Socket Server set up with IP of Computer and listen for Clients
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP = get_ip()
server_address = (IP, 5000)
sock.bind(server_address)
sock.listen(1)



# Set up GPIO preferences
GPIO.cleanup()
GPIO.setwarnings(False)           #do not show any warnings
GPIO.setmode (GPIO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as GPIO19)

# Set up some variables for easy testing
motorSpeed = 10 # 0-100
bufferSize = 10 # range for stopping at motor position
CHANNEL1 = 0
CHANNEL2 = 1
CHANNEL3 = 2
CHANNEL4 = 3

CHANNEL5 = 4 
CHANNEL6 = 5
CHANNEL7 = 6
CHANNEL8 = 7

cheekDir = 26
eyesDir = 27
eyelidsDir = 17
mouthDir = 6

#Cheeks pins				#we are programming the GPIO by BCM pin numbers. (PIN35 as GPIO19)
GPIO.setup(19,GPIO.OUT)           	# initialize GPIO19 as an output.
pCheek = GPIO.PWM(19,100)          		#GPIO19 as PWM output, with 100Hz frequency
pCheek.start(0)
GPIO.setup(cheekDir,GPIO.OUT)				#GPIO26 as direction pin	

#Eyeball Pins
GPIO.setup(22,GPIO.OUT)           	# initialize GPIO22 as an output.
pEyes = GPIO.PWM(22,100)          		#GPIO22 as PWM output, with 100Hz frequency
pEyes.start(0)
GPIO.setup(eyesDir,GPIO.OUT)				#GPIO27 as direction pin	

#Eyelid pins
GPIO.setup(13,GPIO.OUT)           	# initialize GPIO4 as an output.
pEyelids = GPIO.PWM(13,100)          		#GPIo as PWM output, with 100Hz frequency  
pEyelids.start(0)
GPIO.setup(eyelidsDir,GPIO.OUT)				#GPIO17 as direction pin

#Mouth open pins
GPIO.setup(5,GPIO.OUT)           	# initialize GPIO5 as an output.
pMouth = GPIO.PWM(5,100)          		#GPIO5 as PWM output, with 100Hz frequency
pMouth.start(0)
GPIO.setup(mouthDir,GPIO.OUT)				#GPIO6 as direction pin		

# set up the SPI interface pins for the MCP3008
SPICLK = 18
SPIMISO = 23
SPIMOSI = 24
SPICS = 25
GPIO.setup(SPIMOSI, GPIO.OUT)
GPIO.setup(SPIMISO, GPIO.IN)
GPIO.setup(SPICLK, GPIO.OUT)
GPIO.setup(SPICS, GPIO.OUT)

# read SPI data from MCP3008 chip, 8 possible adc's (0 thru 7)
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
	if ((adcnum > 7) or (adcnum < 0)):
			return -1
	GPIO.output(cspin, True)

	GPIO.output(clockpin, False)  # start clock low
	GPIO.output(cspin, False)     # bring CS low

	commandout = adcnum
	commandout |= 0x18  # start bit + single-ended bit
	commandout <<= 3    # we only need to send 5 bits here
	for i in range(5):
			if (commandout & 0x80):
					GPIO.output(mosipin, True)
			else:
					GPIO.output(mosipin, False)
			commandout <<= 1
			GPIO.output(clockpin, True)
			GPIO.output(clockpin, False)

	adcout = 0
	# read in one empty bit, one null bit and 10 ADC bits
	for i in range(12):
			GPIO.output(clockpin, True)
			GPIO.output(clockpin, False)
			adcout <<= 1
			if (GPIO.input(misopin)):
					adcout |= 0x1

	GPIO.output(cspin, True)
	
	adcout >>= 1       # first bit is 'null' so drop it
	return adcout
	
def readADC(adcChannel):
	return readadc(adcChannel, SPICLK, SPIMOSI, SPIMISO, SPICS)
'''	
#Current Sensing - does not work due to random adc readings
def safetyCheek():
	currentSum = 0
	for x in range(50):
		currentSum += readADC(CHANNEL5)
	current = currentSum/50
	print current
	if current > 180:
		pCheek.ChangeDutyCycle(0)
		pEyes.ChangeDutyCycle(0)
		pEyelids.ChangeDutyCycle(0)
		pMouth.ChangeDutyCycle(0)
		print "Stalled Motor Shutting off"
		return True
	return False
	
def safetyEyes():
	currentSum = 0
	for x in range(50):
		currentSum += readADC(CHANNEL6)
	current = currentSum/50
	print current
	if current > 130:
		pCheek.ChangeDutyCycle(0)
		pEyes.ChangeDutyCycle(0)
		pEyelids.ChangeDutyCycle(0)
		pMouth.ChangeDutyCycle(0)
		print "Stalled Motor Shutting off"
		return True
	return False
	
def safetyEyelids():
	currentSum = 0
	for x in range(50):
		currentSum += readADC(CHANNEL7)
	current = currentSum/50
	print current
	if current > 30:
		pCheek.ChangeDutyCycle(0)
		pEyes.ChangeDutyCycle(0)
		pEyelids.ChangeDutyCycle(0)
		pMouth.ChangeDutyCycle(0)
		print "Stalled Motor Shutting off"
		return True
	return False
	
def safetyMouth():
	currentSum = 0
	for x in range(50):
		currentSum += readADC(CHANNEL8)
	current = currentSum/50
	print current
	if current > 25:
		pCheek.ChangeDutyCycle(0)
		pEyes.ChangeDutyCycle(0)
		pEyelids.ChangeDutyCycle(0)
		pMouth.ChangeDutyCycle(0)
		print "Stalled Motor Shutting off"
		return True
	return False		
'''
def shutdown():
		pCheek.ChangeDutyCycle(0)
		pEyes.ChangeDutyCycle(0)
		pEyelids.ChangeDutyCycle(0)
		pMouth.ChangeDutyCycle(0)
		print "Stalled Motor shutting off"
	

def moveMotor(desiredLocation,pinPWM, pinDir, Channel):
	start = time.time()
	currentLocation = readADC(Channel)
	while(currentLocation < desiredLocation-bufferSize or currentLocation > desiredLocation+bufferSize):
		if (currentLocation > desiredLocation+bufferSize):
			GPIO.output(pinDir, GPIO.HIGH)
		if (currentLocation < desiredLocation-bufferSize):
			GPIO.output(pinDir, GPIO.LOW)
		currentLocation = readADC(Channel)
		pinPWM.ChangeDutyCycle(motorSpeed)
		end = time.time()
		if (end - start) > 3:
			shutdown()
			break
	pinPWM.ChangeDutyCycle(0)
	
def moveEyelids(desiredLocation,pinPWM, pinDir, Channel):
	start  = time.time()
	currentLocation = readADC(Channel)
	while(currentLocation < desiredLocation-bufferSize or currentLocation > desiredLocation+bufferSize):
		if (currentLocation > desiredLocation+bufferSize):
			GPIO.output(pinDir, GPIO.LOW)
		if (currentLocation < desiredLocation-bufferSize):
			GPIO.output(pinDir, GPIO.HIGH)
		currentLocation = readADC(Channel)
		pinPWM.ChangeDutyCycle(30)
		end = time.time()
		if (end - start) > 3:
			shutdown()
			break
	pinPWM.ChangeDutyCycle(0)
	
def blink():
	moveEyelids(725,pEyelids, eyelidsDir,CHANNEL3) 
	time.sleep(.1)
	moveEyelids(320,pEyelids, eyelidsDir,CHANNEL3)

def reactNeutral():
	#blink()
	moveMotor(475,pCheek, cheekDir,CHANNEL1) 
	moveEyelids(320,pEyelids, eyelidsDir,CHANNEL3) 
	moveMotor(475,pMouth, mouthDir,CHANNEL4) 
	moveMotor(490,pEyes, eyesDir,CHANNEL2)
	time.sleep(1)
	moveMotor(580,pEyes, eyesDir,CHANNEL2)
	time.sleep(1)
	moveMotor(535,pEyes, eyesDir,CHANNEL2)

def reactHappy():	
	#blink()
	moveMotor(300,pCheek, cheekDir,CHANNEL1) 
	moveEyelids(320,pEyelids, eyelidsDir,CHANNEL3) 
	moveMotor(500,pMouth, mouthDir,CHANNEL4) 
	moveMotor(535,pEyes, eyesDir,CHANNEL2)

def reactAngry():
	#blink()
	moveMotor(640,pCheek, cheekDir,CHANNEL1) 
	moveEyelids(500,pEyelids, eyelidsDir, CHANNEL3)
	moveMotor(480,pMouth, mouthDir,CHANNEL4) 
	moveMotor(544,pEyes, eyesDir,CHANNEL2)

def reactSad():
	#blink()
	moveMotor(640,pCheek, cheekDir,CHANNEL1) 
	moveEyelids(500,pEyelids, eyelidsDir, CHANNEL3)
	moveMotor(400,pMouth, mouthDir,CHANNEL4) 
	moveMotor(517,pEyes, eyesDir,CHANNEL2)

def reactSurprised():
	#blink()
	moveMotor(300,pCheek, cheekDir,CHANNEL1) 
	moveEyelids(320,pEyelids, eyelidsDir,CHANNEL3) 
	moveMotor(500,pMouth, mouthDir,CHANNEL4) 
	moveMotor(535,pEyes, eyesDir,CHANNEL2)
	
def talk():
	
	#Continue running until we kill it
	while conf.running:
		if conf.talking == True: #If its talking, move the mouth
			moveMotor(550,pMouth, mouthDir,CHANNEL4) 
			time.sleep(.25)
			moveMotor(400,pMouth, mouthDir,CHANNEL4) 
			time.sleep(.25)
	
def thread_blink():
	i = 0
	while conf.running:
		blink()
		time.sleep(3.5)
		i = i +1
		if i%3 == 0:
			moveMotor(500,pEyes, eyesDir,CHANNEL2)
			time.sleep(0.1)
			moveMotor(570,pEyes, eyesDir,CHANNEL2)
			time.sleep(0.1)
			moveMotor(535,pEyes, eyesDir,CHANNEL2)
		
def stopTalking():
	moveMotor(400,pMouth, mouthDir,CHANNEL4)
	
# Sever Accepts Client and Controls Face based on recived data


'''
def StartTalk(i):
		while i == '6':
			talk()
'''
"""
while True:
    connection, client_address = sock.accept()
    print("accepted")
    while True:
        try:
            data = connection.recv(20)
            if not data: break
            
            if data =='1':
                reactNeutral()
            if data == '2':
                reactHappy()
            if data =='3':
                reactAngry()
            if data =='4':
                reactSad()
            if data == '5':
                reactSurprised()
            if data == '6':
				talk()

        except:
            sock.close()
'''         
mythread = mp.Process(target=StartTalk('6'))
mythread.start()
time.sleep(1)
mythread.terminate()
mythread.cancel()
'''
sock.close()
"""
