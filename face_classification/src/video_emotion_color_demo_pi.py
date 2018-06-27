#!/usr/bin/env python
from statistics import mode
import speech_recognition as sr
import cv2
from keras.models import load_model
import numpy as np
import os
import time
import sys
import socket

from utils.datasets import get_labels
from utils.inference import detect_faces
from utils.inference import draw_text
from utils.inference import draw_bounding_box
from utils.inference import apply_offsets
from utils.inference import load_detection_model
from utils.preprocessor import preprocess_input
from utils.chat import *
from picamera import PiCamera
from picamera.array import PiRGBArray

camera = PiCamera()
camera.resolution=(640,480)
camera.framerate = 32
camera.rotation = 180
rawCapture = PiRGBArray(camera, size=(640,480))
time.sleep(0.1)


# IP adress of computer connectiong to
IP= ''
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (IP, 10000)


def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    # check that recognizer and microphone arguments are appropriate type
    if not isinstance(recognizer, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")

    if not isinstance(microphone, sr.Microphone):
        raise TypeError("`microphone` must be `Microphone` instance")

    # adjust the recognizer sensitivity to ambient noise and record audio
    # from the microphone
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly
    try:
        response["transcription"] = recognizer.recognize_google(audio)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"

    return response

# parameters for loading data and images
detection_model_path = '../trained_models/detection_models/haarcascade_frontalface_default.xml'
emotion_model_path = '../trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5'
emotion_labels = get_labels('fer2013')

# hyper-parameters for bounding boxes shape
frame_window = 10
emotion_offsets = (20, 40)

# loading models
face_detection = load_detection_model(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)

# getting input model shapes for inference
emotion_target_size = emotion_classifier.input_shape[1:3]

# starting lists for calculating modes
emotion_window = []

# starting video streaming
cv2.namedWindow('window_frame')


#creating voice recognizer and microphone
recognizer = sr.Recognizer()
#use sr.Microphone.list_microphone_names() to find the device index
#if device_index arg is omitted, it will use the default microphone
microphone = sr.Microphone()

# connect to socket server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(server_address)

#Chatbot introduction
intro = "Hello, I am Herbot A. Simon. I am a social robot who can detect emotion and respond accordingly."
print(intro)
os.system('echo %s | festival --tts' % intro) 
	
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    for i in range(1,10):
        bgr_image = frame.array
        rawCapture.truncate(0)
        bgr_image = cv2.resize(bgr_image, (600, 600))
        gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
        rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
        faces = detect_faces(face_detection, gray_image)

    for face_coordinates in faces:
        x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
        gray_face = gray_image[y1:y2, x1:x2]
        try:
            gray_face = cv2.resize(gray_face, (emotion_target_size))
        except:
            continue

        gray_face = preprocess_input(gray_face, True)
        gray_face = np.expand_dims(gray_face, 0)
        gray_face = np.expand_dims(gray_face, -1)
        emotion_prediction = emotion_classifier.predict(gray_face)
        emotion_probability = np.max(emotion_prediction)
        emotion_label_arg = np.argmax(emotion_prediction)
        emotion_text = emotion_labels[emotion_label_arg]
        emotion_window.append(emotion_text)

        if len(emotion_window) > frame_window:
            emotion_window.pop(0)
        try:
            emotion_mode = mode(emotion_window)
        except:
            continue

        if emotion_text == 'angry':
	        color = emotion_probability * np.asarray((255, 0, 0))
	        sock.send("3".encode())
	        prompt = get_prompt(emotion_text)
	        print(prompt)
	        os.system('echo %s | festival --tts' % prompt) 
	        #os.system('echo "Why are you so angry?" | festival --tts') 
	        #print("Why are you so angry?\n")
	        response = recognize_speech_from_mic(recognizer, microphone)
	        if not response["success"]:
	            print("I didn't catch that. What did you say?\n")
	        if response["error"]:
	    	    print("ERROR: {}".format(response["error"]))
	    	    break
	        print("You said: {}".format(response["transcription"]))
	        botResp = respond(response["transcription"])
	        print(botResp)
	        os.system('echo %s | festival --tts' % botResp) 
        elif emotion_text == 'sad':
	        color = emotion_probability * np.asarray((0, 0, 255))
	        sock.send("4".encode())
	        prompt = get_prompt(emotion_text)
	        print(prompt)
	        os.system('echo %s | festival --tts' % prompt) 
	        #os.system('echo "Why the long face?" | festival --tts') 
	        #print("Why the long face?\n")
	        response = recognize_speech_from_mic(recognizer, microphone)
	        if not response["success"]:
	            print("I didn't catch that. What did you say?\n")
	        if response["error"]:
	    	    print("ERROR: {}".format(response["error"]))
	    	    break
	        print("You said: {}".format(response["transcription"]))
	        botResp = respond(response["transcription"])
	        print(botResp)
	        os.system('echo %s | festival --tts' % botResp) 
        elif emotion_text == 'happy':
	        color = emotion_probability * np.asarray((255, 255, 0))
	        sock.send("2".encode())
	        prompt = get_prompt(emotion_text)
	        print(prompt)
	        os.system('echo %s | festival --tts' % prompt) 
	        #os.system('echo "You seem happy today. How are you?" | festival --tts') 
	        #print("You seem happy today. How are you?\n")
	        response = recognize_speech_from_mic(recognizer, microphone)
	        if not response["success"]:
	            print("I didn't catch that. What did you say?\n")
	        if response["error"]:
	            print("ERROR: {}".format(response["error"]))
	            break
	        print("You said: {}".format(response["transcription"]))
	        botResp = respond(response["transcription"])
	        print(botResp)
	        os.system('echo %s | festival --tts' % botResp) 
        elif emotion_text == 'surprise':
	        color = emotion_probability * np.asarray((0, 255, 255))
	        sock.send("5".encode())
	        prompt = get_prompt(emotion_text)
	        print(prompt)
	        os.system('echo %s | festival --tts' % prompt) 
	        #os.system('echo "Did I surprise you?" | festival --tts') 
	        #print("Did I surprise you?\n")
	        response = recognize_speech_from_mic(recognizer, microphone)
	        if not response["success"]:
	            print("I didn't catch that. What did you say?\n")
	        if response["error"]:
	            print("ERROR: {}".format(response["error"]))
	            break
	        print("You said: {}".format(response["transcription"]))
	        botResp = respond(response["transcription"])
	        print(botResp)
	        os.system('echo %s | festival --tts' % botResp) 
        elif emotion_text == 'neutral':
	        color = emotion_probability * np.asarray((0, 255, 255))
	        sock.send("1".encode())
	        prompt = get_prompt(emotion_text)
	        print(prompt)
	        os.system('echo %s | festival --tts' % prompt) 
	        #os.system('echo "You seem pretty neutral today. How are you?" | festival --tts') 
	        #print("You seem pretty neutral today. How are you?\n")
	        response = recognize_speech_from_mic(recognizer, microphone)
	        if not response["success"]:
	            print("I didn't catch that. What did you say?\n")
	        if response["error"]:
	            print("ERROR: {}".format(response["error"]))
	            break
	        print("You said: {}".format(response["transcription"]))
	        botResp = respond(response["transcription"])
	        print(botResp)
	        os.system('echo %s | festival --tts' % botResp) 
        else:
	        color = emotion_probability * np.asarray((0, 255, 0))

        color = color.astype(int)
        color = color.tolist()

        draw_bounding_box(face_coordinates, rgb_image, color)
        draw_text(face_coordinates, rgb_image, emotion_mode,
                  color, 0, -45, 1, 1)

    bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    cv2.imshow('window_frame', bgr_image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
