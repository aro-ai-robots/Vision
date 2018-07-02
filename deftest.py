def EmotionResponse(emotion_to_respond):
	promt = get prompt(emotion_to_respond)
	print(promt)
	time.sleep(sleeper)
	sock.send('6'.encode()
	os.system('echo %s | festival --tts' % prompt) 
	sock.send('7'.encode())
	response = recognize_speech_from_mic(recognizer,microphone)
	if not response["success"]:
		print("I didn't catch that. What did you say?\n")
	if response["error"]:
		print("ERROR: {}".format(response["error"]))
	   	break
	print("You said: {}".format(response["transcription"]))
	botResp = respond(response["transcription"])
	print(botResp)
	sock.send('6'.encode())
	os.system('echo %s | festival --tts' % botResp) 
	sock.send('7'.encode())
