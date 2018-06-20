#!/usr/bin/python
# Head Control

import time
from Tkinter import *

# This starts the GUI graphics
app = Tk()
app.title('Face Adjustment app')
app.geometry('400x300')

# Default settings for all of the motors (initial face configuration)
eyeCloseSetting = 5
eyeSideSetting = 5
mouthCloseSetting = 5
mouthExpressionSetting = 5
eyebrowSetting = 5
neckSetting = 5


# These are functions to controll the orangutans
def eyeControl(val):
    eyeCloseSetting = eyesOpenSlider.get()
    eyeSideSetting = sideSlider.get()
    ledout_val_eye = [0x0f, eyeCloseSetting, 0x05, eyeSideSetting, 0x05, 0x0f, 0x00]
    print val
    


def mouthControl(val):
    mouthCloseSetting = mouthOpenSlider.get()
    mouthExpressionSetting = expSlider.get()
    ledout_val_mouth = [0x0f, mouthCloseSetting, 0x05, mouthExpressionSetting, 0x05, 0x0f, 0x00]
    print val


# This is the code for the sliders
# Eye Open
eyeOpenLabel = Label(app, text = 'Eye Open or Shut')
eyeOpenLabel.pack()

eyeOpenSlider = Scale(app, from_=0, to=10, orient = HORIZONTAL, command=eyeControl)
eyeOpenSlider.set(5)
eyeOpenSlider.pack()

#Eye Positioning
sideLabel = Label(app, text = 'Eye Side')
sideLabel.pack()

sideSlider = Scale(app, from_=0, to=10, orient = HORIZONTAL, command=eyeControl)
sideSlider.set(5)
sideSlider.pack()

#Mouth Open/Close (not working)
mouthOpenLabel = Label(app, text = 'Mouth Open')
mouthOpenLabel.pack()

mouthOpenSlider = Scale(app, from_=0, to=10, orient = HORIZONTAL, command=mouthControl)
mouthOpenSlider.set(5)
mouthOpenSlider.pack()

#MouthPositioning
expLabel = Label(app, text = 'Mouth Expression')
expLabel.pack()

expSlider = Scale(app, from_=0, to=10, orient = HORIZONTAL, command=mouthControl)
expSlider.set(5)
expSlider.pack()

app.mainloop()



