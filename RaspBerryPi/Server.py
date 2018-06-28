import socket
import sys

#this function grabs the IP address of the machine running the server
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

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP of your computer
IP = get_ip()
server_address = (IP, 5000)
sock.bind(server_address)
sock.listen(1)

while True:
    connection, client_address = sock.accept()
    print("accepted")
    while True:
        try:
            data = connection.recv(20)
            if not data: break
            print(data)
        except:
            sock.close()

sock.close()

#	to close a port, use...
#		lsof -i :<PORT_NUMBER>
#		sudo kill -9 <PID_NUMBER>
