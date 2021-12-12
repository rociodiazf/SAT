#!/usr/bin/python3

import socket
import random


mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.bind(('localhost', 1234))

# Queue a maximum of 5 TCP connection requests

mySocket.listen(5)

# Accept connections, read incoming data, and answer back an HTML page
#  (in an infinite loop)


while True:
    print('Waiting for connections')
    (recvSocket, address) = mySocket.accept()
    print('HTTP request received:')
    #-- Comenzamos
    file = (recvSocket.recv(1024)).decode("utf-8")

    aleat = random.randint(0, 1000)

    #-- Respuesta
    recvSocket.send(b"HTTP/1.1 200 OK\r\n\r\n" +
                    b"<html><body><h1>Hello World!</h1>" +
                    b"<p><a href= " + bytes(str(aleat), 'utf-8') +
                    #-- Pasamos a string y codificamos
                    #-- The href attribute specifies the link's destination
                    b">Dame otra</a> "+
                    b"</p>" +
                    b"</body></html>" +
                    b"\r\n")
    recvSocket.close()
