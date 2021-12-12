#!/usr/bin/env python3

import random
import webapp

class aleatApp(webapp.webApp):
	def process(self, parsedRequest):

		aleat  = random.randint(0, 10000)
		return ("200 OK", "<html><body><h1><a href=' " + str(aleat) + "'>Dame otra</a></h1></body></html>")

if __name__ == "__main__":
    testWebApp = aleatApp("localhost", 1234)
