'''
'
'USE WITH PYTHON 2.7
'
'''

import socket
import sys

ip_address = input("Enter the IP address of the server: ")
# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = (ip_address, 5000)

while True:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(server_address)
        message=input('Message: ')
        message = message.encode()
        if message=='quit':
            break
        sock.send(message)
    except:
        break
sock.close()
