import speech_recognition as sr

r = sr.Recognizer()
mic = sr.Microphone(device_index = 6)
with mic as source:
	audio = r.listen(source)
	
#with mic as source:
#	r.adjust_for_ambient_noise(source)
#	audio = r.listen(source)
	
print(r.recognize_google(audio))


#sr.Microphone.list_microphone_names() this is to find what device you want
