import socket
import sys
import cv2
import numpy as np

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
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
            print("bad")
            sock.close()
sock.close()
        
