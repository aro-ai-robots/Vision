#!/usr/bin/python
# Head Control

import time
from Tkinter import *
import RPi.GPIO as GPIO

# Set up GPIO preferences

GPIO.setwarnings(False)           #do not show any warnings
GPIO.setmode (GPIO.BCM)         #we are programming the GPIO by BCM pin numbers. (PIN35 as GPIO19)

# Set up some variables for easy testing
motorSpeed = 20 # 0-100
bufferSize = 10 # range for stopping at motor position
CHANNEL1 = 0
CHANNEL2 = 1
CHANNEL3 = 2
CHANNEL4 = 3
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
GPIO.setup(5,GPIO.OUT)           	# initialize GPIO5 as an output. 5
pMouth = GPIO.PWM(5,100)          		#GPIO5 as PWM output, with 100Hz frequency
pMouth.start(0)
GPIO.setup(mouthDir,GPIO.OUT)				#GPIO6 as direction pin		

#Neck Servo
GPIO.setup(4, GPIO.OUT)
pNeck = GPIO.PWM(4, 50)
pNeck.start(0)

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

def moveMotor(desiredLocation,pinPWM, pinDir, Channel):
	currentLocation = readADC(Channel)
	while(currentLocation < desiredLocation-bufferSize or currentLocation > desiredLocation+bufferSize):
		if (currentLocation > desiredLocation+bufferSize):
			GPIO.output(pinDir, GPIO.HIGH)
		if (currentLocation < desiredLocation-bufferSize):
			GPIO.output(pinDir, GPIO.LOW)
		currentLocation = readADC(Channel)
		pinPWM.ChangeDutyCycle(motorSpeed)
	pinPWM.ChangeDutyCycle(0)

def moveEyelids(desiredLocation,pinPWM, pinDir, Channel):
	currentLocation = readADC(Channel)
	while(currentLocation < desiredLocation-bufferSize or currentLocation > desiredLocation+bufferSize):
		if (currentLocation > desiredLocation+bufferSize):
			GPIO.output(pinDir, GPIO.LOW)
		if (currentLocation < desiredLocation-bufferSize):
			GPIO.output(pinDir, GPIO.HIGH)
		currentLocation = readADC(Channel)
		pinPWM.ChangeDutyCycle(motorSpeed)
	pinPWM.ChangeDutyCycle(0)

def cheekControl(val): 
    slideVal = cheekSlider.get()
    loc = slideVal * 35 + 300 
    moveMotor(loc, pCheek, cheekDir, CHANNEL1)

def eyesControl(val):
    slideVal = eyesSlider.get()
    loc = slideVal * 9 + 490
    moveMotor(loc, pEyes, eyesDir, CHANNEL2)

def eyelidsControl(val):
    slideVal = eyelidsSlider.get()
    loc = slideVal * 45 + 275
    moveEyelids(loc, pEyelids, eyelidsDir, CHANNEL3)

def mouthControl(val):
    slideVal = mouthSlider.get()
    loc = slideVal * 27 + 400
    moveMotor(loc, pMouth, mouthDir, CHANNEL4)

def neckControl(val):
    slideVal = neckSlider.get()
    angle = slideVal 
    duty = float(angle) + 2.5
    pNeck.ChangeDutyCycle(duty)

# change these as desired - they're the pins connected from the
# SPI port on the ADC to the Cobbler

app = Tk()
app.title('Face Adjustment app')
app.geometry('400x300')

#Cheek Slider
cheekLabel = Label(app, text = 'Cheeks')
cheekLabel.pack()
cheekSlider = Scale(app, from_=0, to=10, orient = HORIZONTAL, command=cheekControl)
cheekSlider.set(5)
cheekSlider.pack()

#eyes Slider
eyesLabel = Label(app, text = 'Eyes')
eyesLabel.pack()
eyesSlider = Scale(app, from_=0, to=10, orient = HORIZONTAL, command=eyesControl)
eyesSlider.set(5)
eyesSlider.pack()

#eyelids Slider
eyelidsLabel = Label(app, text = 'Eyelids')
eyelidsLabel.pack()
eyelidsSlider = Scale(app, from_=0, to=10, orient = HORIZONTAL, command=eyelidsControl)
eyelidsSlider.set(1)
eyelidsSlider.pack()

#Mouth Slider
mouthLabel = Label(app, text = 'Mouth')
mouthLabel.pack()
mouthSlider = Scale(app, from_=0, to=10, orient = HORIZONTAL, command=mouthControl)
mouthSlider.set(5)
mouthSlider.pack()

#Neck Slider
neckLabel = Label(app, text = 'Neck')
neckLabel.pack()
neckSlider = Scale(app, from_=0, to=10, orient = HORIZONTAL, command=neckControl)
neckSlider.set(5)
neckSlider.pack()

try:
	app.mainloop()
except KeyboardInterrupt:
	print "Exception"

	
finally:
	GPIO.cleanup()
