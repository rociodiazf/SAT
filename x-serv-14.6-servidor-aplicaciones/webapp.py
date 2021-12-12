#!/usr/bin/python3

import socket

def dihola():
    return("hola")

class webApp():

    def parse(self, request):
        """Parse the received request, extracting the relevant information."""

        return None

    def process(self, parsedRequest):
        """Process the relevant elements of the request.

        Returns the HTTP code for the reply, and an HTML page.
        """

        return ("200 OK", "<html><body><h1>It's works!</h1></body></html>")

    def __init__(self, hostname, port):
        """Initialize the web application."""

        # Create a TCP objet socket and bind it to a port
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        mySocket.bind((hostname, port))

        # Queue a maximum of 5 TCP connection requests
        mySocket.listen(5)

        # Accept connections, read incoming data, and call
        # parse and process methods (in a loop)

        while True:
            print('Waiting for connections')
            (recvSocket, address) = mySocket.accept()
            print('HTTP request received (going to parse and process):')
            request = str(recvSocket.recv(2048))
            print(request)
            parsedRequest = self.parse(request)
            (returnCode, htmlAnswer) = self.process(parsedRequest)
            print(returnCode)
            print('Answering back...')
            recvSocket.send(b"HTTP/1.1 " + bytes(returnCode, "utf-8") + b" \r\n\r\n"
                            + bytes(htmlAnswer, "utf-8") + b"\r\n")
            recvSocket.close()

if __name__ == "__main__":
    testWebApp = webApp("localhost", 1234)
