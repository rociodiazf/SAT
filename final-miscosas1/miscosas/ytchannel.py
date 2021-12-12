from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import string

class YTHandler(ContentHandler):


    def __init__ (self):
        # Item
        self.inEntry = False
        self.inContent = False
        self.content = ""
        self.title = " "
        self.link = " "
        self.description = " "
        self.id = ""
        self.videos = []
        # Alimentador
        self.nameAlim = " "
        self.uriAlim = " "


    def startElement (self, name, attrs):
        if name == 'entry':
            self.inEntry = True
        elif self.inEntry:
            if name == 'title':
                self.inContent = True
            elif name == 'link':
                self.link = attrs.get('href')
            elif name == 'media:description':
                self.inContent = True
            elif name == 'yt:videoId':
                self.inContent = True
        elif not self.inEntry:
            if name == 'title':
                self.inContent = True
            elif name == 'uri':
                self.inContent = True


    def endElement (self, name):
        global videos

        if name == 'entry':
            self.inEntry = False
            self.videos.append({'link': self.link,
                                'title': self.title,
                                'description': self.description,
                                'id': self.id})
        elif self.inEntry:
            if name == 'title':
                self.title = self.content
                self.content = ""
                self.inContent = False
            elif name == 'media:description':
                self.description = self.content
                self.content = ""
                self.inContent = False
            elif name == 'yt:videoId':
                self.id = self.content
                self.content = ""
                self.inContent = False

    # Iformacion relacionada con el canal
        elif not self.inEntry:
            if name == 'title':
                self.nameAlim = self.content
                self.content = ""
                self.inContent = False
            elif name == 'uri':
                self.uriAlim = self.content
                self.content = ""
                self.inContent = False


    def characters (self, chars):
        if self.inContent:
            self.content = self.content + chars

class YTChannel:

    def __init__(self, stream):
        self.parser = make_parser()
        self.handler = YTHandler()
        self.parser.setContentHandler(self.handler)
        self.parser.parse(stream)

    def videos (self):
        return self.handler.videos

    def nameAlim (self):
        return self.handler.nameAlim

    def uriAlim (self):
        return self.handler.uriAlim
