# Einstein
The base emotion and gender classification program is from the the B-IT-BOTS robotics team. https://github.com/oarriaga/face_classification

The chatbot is based on brobot by Liza Daly: https://github.com/lizadaly/brobot

This program is meant to be a simple chatbot based on the user's emotions. The chatbot will make a simple conversation with the reader based on its initial impression of the user's emotions. The program continues to loop after each conversation.

## Installation instructions for Ubuntu
We are assuming that python3 and pip3 are installed on your computer.
*When using pip install, use pip3 rather than pip.

Install Opencv and Contrib: 
https://www.pyimagesearch.com/2016/10/24/ubuntu-16-04-how-to-install-opencv/ 

Install Keras, Tensorflow, and dependencies: 
https://www.pyimagesearch.com/2016/07/18/installing-keras-for-deep-learning/ 

Install Festival: 
```
sudo apt-get install festival festvox-kallpc16k

Sudo apt-get install festival
```

Install Pandas:

`sudo apt-get install python3-pandas`


Install Speech Recognition and Pyaudio by following the tutorial:
*Make sure to use pip3 rather than pip to install anything and use python3 as your interpreter instead of default python.

https://realpython.com/python-speech-recognition/#


Install textblob:
```
pip3 install -U textblob

python3 -m textblob.download_corpora
```

Clone the repository from github:
Git clone https://github.com/aro-ai-robots/Vision.git 
	
Cd ~/Vision-master/face_classification/src$

Run:
`python3 video_emotion_color_demo.py`


## Wiring Documentation  

  
**On Motor Controller:**

Channel 1 maps to Cheeks motor

Channel 2 maps to Eyeballs motor

Channel 3 maps to Eyelids motor

Channel 4 maps to Mouth motor


   
**From Motor Controller Channels to Breadboard and Cobbler**

Channel 1:

PWM (blue) --> pin 19

DIR (yellow) --> pin 26

GND (gray) --> GND


Channel 2:

PWN (blue) --> pin 22

DIR (yellow) --> pin 27

GND (gray) --> GND


Channel 3:

PWN (blue) --> pin 13

DIR (yellow) --> pin 17

GND (gray) --> GND


Channel 4:

PWN (blue) --> pin 5

DIR (yellow) --> pin 6

GND (gray) --> GND

    
**ADC Installation and Wiring**

Wiring Diagram from: https://learn.adafruit.com/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi/connecting-the-cobbler-to-a-mcp3008

Install Required packages from: https://learn.adafruit.com/reading-a-analog-in-and-controlling-audio-volume-with-the-raspberry-pi/necessary-packages  

The adc mcp chip channels run from top to bottom, meaning Channel 0 is the first row. 
  
Cheeks maps to Channel 0 on adc mcp chip

Eyeballs maps to Channel 1 on adc mcp chip

Eyelids maps to Channel 2 on adc mcp chip

Mouth maps to Channel 3 on adc mcp chip

cd `Vision` and run `python Main.py`

**Wiring Diagram**

https://github.com/aro-ai-robots/Vision/blob/master/einstein.png
