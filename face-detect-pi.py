import cv2
import sys
from picamera.array import PiRGBArray
from picamera import PiCamera
import time


camera = PiCamera()
camera.resolution=(640,480)
camera.framerate = 32
rawCapture = PiRGBArray(camera, size=(640,480))




cascPath = sys.argv[0]
faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Capture frame-by-frame
    frame = frame.array
    rawCapture.truncate(0)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        
    )

    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Display the resulting frame
    cv2.imshow('Video', frame)
    
    # To quit the program press q
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
