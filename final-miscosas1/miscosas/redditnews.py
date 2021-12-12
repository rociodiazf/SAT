from xml.sax.handler import ContentHandler
from xml.sax import make_parser
import sys
import string

class RedditHandler(ContentHandler):


    def __init__ (self):
        # Item
        self.inEntry = False
        self.inContent = False
        self.content = ""
        self.title = " "
        self.link = " "
        self.description = " "
        self.id = " "
        self.news = []
        # Alimentador
        self.nameAlim = " "
        self.uriAlim = " "


    def startElement (self, name, attrs):
        if name == 'entry':
            self.inEntry = True
        elif self.inEntry:
            if name == 'content':
                self.inContent = True
            elif name == 'link':
                self.link = attrs.get('href')
            elif name == 'title':
                self.inContent = True
            elif name == 'id':
                self.inContent = True
        elif not self.inEntry:
            if name == 'title':
                self.inContent = True
            elif (name == 'link') and (attrs.get('rel') == "alternate"):
                self.uriAlim = attrs.get('href')


    def endElement (self, name):
        global news

        if name == 'entry':
            self.inEntry = False
            self.news.append({'link': self.link,
                                'title': self.title,
                                'description': self.description,
                                'id':self.id})
        elif self.inEntry:
            if name == 'title':
                self.title = self.content
                self.content = ""
                self.inContent = False
            elif name == 'content':
                self.description = self.content
                self.content = ""
                self.inContent = False
            elif name == 'id':
                self.id = self.content
                self.content = ""
                self.inContent = False
    # Iformacion relacionada con el canal
        elif not self.inEntry:
            if name == 'title':
                self.nameAlim = self.content
                self.content = ""
                self.inContent = False


    def characters (self, chars):
        if self.inContent:
            self.content = self.content + chars

class RedditNews:

    def __init__(self, stream):
        self.parser = make_parser()
        self.handler = RedditHandler()
        self.parser.setContentHandler(self.handler)
        self.parser.parse(stream)

    def news (self):
        return self.handler.news

    def nameAlim (self):
        return self.handler.nameAlim

    def uriAlim (self):
        return self.handler.uriAlim
