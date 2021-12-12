#!/usr/bin/python3

import socket
import webapp

class adiosApp(webapp.webApp):

#-- Overide
    def process (self, parsedRequest):
        #-- Process the new answer
        return ("200 OK", "<html><body><h1>Hola Mundo!</h1></body></html>")



if __name__ == "__main__":
    testAdiosApp = adiosApp("localhost", 1234)
