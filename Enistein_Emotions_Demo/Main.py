import socket
import threading as th
from emotionalStates import *
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

server_address = (IP, 4000)
sock.bind(server_address)
sock.listen(1)

#build the thread for the talking mechanism
talkiing_thread = th.Thread(target = talk)
blinking_thread = th.Thread(target = thread_blink)
my_bool = False #Prevents restarting a running thread


try:
	while True:
		connection, client_address = sock.accept()
		print("accepted")
		
		#This block only runs oonce dispite being in a while loop
		if not my_bool:
			print("Starting threads")
			talkiing_thread.start() #Start the threads
			blinking_thread.start()
			print("Threads is started")
			my_bool = True 
			
		
		while True:
			
			#Try to get the data and the sort the signal to the 
			#corrisponding function
			try:
				data = connection.recv(20)
				if (not data):
					break
				elif data =='1':
					reactNeutral()
				elif data == '2':
					reactHappy()
				elif data =='3':
					reactAngry()
				elif data =='4':
					reactSad()
				elif data == '5':
					reactSurprised()
				elif data =='6':
					conf.talking = True
				elif data == '7':
					conf.talking = False
			except:
				print("ERROR")
				sock.close()
				break #?
	sock.close()
	
#If there was an interupt, stop the thread
except KeyboardInterrupt:
	conf.running = False
	pass
except: 
	print "Exception happened"	
finally: 
	GPIO.cleanup()
	
