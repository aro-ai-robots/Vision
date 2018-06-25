import socket
import sys
import cv2
import numpy as np
from picamera.array import PiRGBArray
from picamera import PiCamera
import time


camera = PiCamera()
camera.resolution=(640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640,480))

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
