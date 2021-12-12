#!/usr/bin/python3
"""
Simple HTTP Server
Jesus M. Gonzalez-Barahona and Gregorio Robles
{jgb, grex} @ gsyc.es
SAT and SARO subjects (Universidad Rey Juan Carlos)
"""

import socket
import operator as op
import calcu


# Create a TCP objet socket and bind it to a port
# We bind to 'localhost', therefore only accepts connections from the
# same machine
# Port should be 80, but since it needs root privileges,
# let's use one above 1024

mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket.bind(('localhost', 1235))

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


    file = file.split('\n')

    line = file[0]
    words = line.split('/')

    #-- Separamos lo recivido
    operation = words[1]
    if operation in calcu.dic:

        op_1 = words[2]
        op_2 = words[3]
        op_2 = op_2[0]


        #-- Debemos tener en cuenta de que me esta enviando int o float.
        try:
            op_1 = int(op_1)
            op_2 = int(op_2)
        except ValueError:
            sys.exit("Operands must be numbers")

        if op_2 == 0:
            sys.exit ("Can't divided by 0")

        resultado = calcu.dic[operation](op_1, op_2)
        print("El resultado de la operacion es: " + str(resultado))

        #-- Respuesta
        recvSocket.send(b"HTTP/1.1 200 OK\r\n\r\n" +
                        b"<html><body>Resultado!: </body></html>" +
                        bytes(str(resultado),"utf-8")+
                        b"\r\n")
        recvSocket.close()
