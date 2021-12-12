#!/usr/bin/python3

#
# Simple XML parser for YouTube XML channels
# Jesus M. Gonzalez-Barahona
# jgb @ gsyc.es
# SARO and SAT subjects (Universidad Rey Juan Carlos)
# 2020
#
# Produces a HTML document in standard output, with
# the list of videos on the channel
#
# How to get the XML document for a YouTube channel:
# https://www.youtube.com/feeds/videos.xml?channel_id=UC300utwSVAYOoRLEqmsprfg

from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import string

videos = ""

class YTHandler(ContentHandler):
    #-- manejador donde he expecualizado el comportamiendo

    def __init__ (self):
        #-- Inilicializacion del objeto.
        self.inEntry = False
        self.inContent = False
        self.content = ""
        self.title = ""
        self.link = ""

    def startElement (self, name, attrs):
        # va a ser llamdo cuando se reconozca el inicio de un elemento
        if name == 'entry':
            self.inEntry = True
            #-- Es una variable <entry></entry>
        elif self.inEntry:
            #-- Si no estoy dentro de un elemento...
            if name == 'title':
                self.inContent = True
                #-- como lo que me interesa es el titulo...
            elif name == 'link':
                #-- leo el atributo y lo meto en la variable link del objeto
                self.link = attrs.get('href')

    def endElement (self, name):
        global videos

        if name == 'entry':#-- final de un entry
            self.inEntry = False
            videos = videos \
                     + "    <li><a href='" + self.link + "'>" \
                     + self.title + "</a></li>\n"
        elif self.inEntry:
            if name == 'title':
                self.title = self.content
                #-- reinicializo el self.content
                self.content = ""
                self.inContent = False

    def characters (self, chars):
        #-- Cuadno este leyendo los caracteres de un elemento terminal
        if self.inContent:
            self.content = self.content + chars

# Load parser and driver

Parser = make_parser()
Parser.setContentHandler(YTHandler())

# --- Main prog
if __name__ == "__main__":

    PAGE = """
<!DOCTYPE html>
<html lang="en">
  <body>
    <h1>Channel contents:</h1>
    <ul>
{videos}
    </ul>
  </body>
</html>
"""
#-- Page: en {videos} vamos a meter la lista de los videos

    if len(sys.argv)<2:
        print("Usage: python xml-parser-youtube.py <document>")
        print()
        print(" <document>: file name of the document to parse")
        sys.exit(1)

    # Ready, set, go!
    xmlFile = open(sys.argv[1],"r")

    Parser.parse(xmlFile)
    #-- Rellenamos el formulario.
    page = PAGE.format(videos=videos)
    #-- Lo mostramos por pantalla
    print(page)
