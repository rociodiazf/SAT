from django.test import TestCase, SimpleTestCase
from django.db.models import QuerySet
from django.template import Template

from . import views
from .ytchannel import YTChannel

class TestYTChannel(SimpleTestCase):
    """Tests of YTChannel"""

    def setUp(self):

        self.simpleFile = 'youtube/testdata/youtube.xml'
        self.zeroFile = 'youtube/testdata/youtube-0.xml'
        self.oneFile = 'youtube/testdata/youtube-1.xml'
        self.expected = [{'link': 'https://www.youtube.com/watch?v=WlqYH7clQ0c',
                     'title': 'Implementación de aplicaciones web: Counter WebApp',
                     'id': 'WlqYH7clQ0c'},
                    {'link': 'https://www.youtube.com/watch?v=FmtWarjh1SQ',
                     'title': 'Implementación de aplicaciones web: Counter Server',
                     'id': 'FmtWarjh1SQ'},
                    {'link': 'https://www.youtube.com/watch?v=6fLZUn5jWjk',
                     'title': 'Arquitectura Modelo-Vista-Controlador',
                     'id': '6fLZUn5jWjk'},
                    {'link': 'https://www.youtube.com/watch?v=nfq8R654D4s',
                     'title': 'Frikiminutos: Proyecto Gutenberg',
                     'id': 'nfq8R654D4s'},
                    {'link': 'https://www.youtube.com/watch?v=Ew37o0oMY80',
                     'title': 'Introducción a Django y "Django calc"',
                     'id': 'Ew37o0oMY80'},
                    {'link': 'https://www.youtube.com/watch?v=IY3dywwiM6g',
                     'title': 'Acceso a los laboratorios docentes de la ETSIT medainte VNCweb y ssh',
                     'id': 'IY3dywwiM6g'}]

    def test_simple(self):
        """Find videos in a simple XML file for a YT channel"""

        xmlFile = open(self.simpleFile, 'r')
        channel = YTChannel(xmlFile)
        videos = channel.videos()
        self.assertEqual(videos, self.expected)

    def test_zero(self):
        """Find videos in a file with no <entry> (only channel data)"""

        xmlFile = open(self.zeroFile, 'r')
        channel = YTChannel(xmlFile)
        videos = channel.videos()
        self.assertEqual(len(videos), 0)

    def test_one(self):
        """Find videos in a file with no <entry> (only channel data)"""

        xmlFile = open(self.oneFile, 'r')
        channel = YTChannel(xmlFile)
        videos = channel.videos()
        self.assertEqual(len(videos), 1)
        self.assertEqual(videos, self.expected[0:1])


class TestViewsMain(TestCase):
    """Tests of main method in views"""

    def setUp(self):
        # Id known to be in the list of videos of the channel
        self.id = 'uBuldIyTo8I'

    def test_get_ok(self):
        """GET / returns OK"""

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_view(self):
        """Check if GET / is served by views.main"""

        response = self.client.get('/')
        self.assertEqual(response.resolver_match.func, views.main)

    def test_get_content(self):
        """Check if content returned by GET / includes some strings"""

        checks = ["<h1>Django YouTube (version 3)</h1>",
                  "<h2>Selected</h2>",
                  "<h2>Selectable</h2>",
                  "<input type='hidden' name='id' value='TKjYnkGGQxs'>"]
        response = self.client.get('/')
        content = response.content.decode(encoding='UTF-8')
        for check in checks:
            self.assertInHTML(check, content)

    def test_get_template(self):
        """Templates used to render response for /"""

        response = self.client.get('/')
        # PAGE and VIDEO are templates used to render response
        self.assertIn(views.PAGE, response.templates)
        self.assertIn(views.VIDEO, response.templates)
        # selected, selectable contexts are QuerySet, video_tmp is Template
        context = response.context
        self.assertIsInstance(context['selected'], QuerySet)
        self.assertIsInstance(context['selectable'], QuerySet)
        self.assertIsInstance(context['video_tmpl'], Template)
        # selected is an empty QuerySet
        self.assertEqual(len(context['selected']), 0)

    def test_post_ok(self):
        """POST to / returns OK"""

        response = self.client.post('/', {'id': self.id})
        self.assertEqual(response.status_code, 200)

    def test_getpost(self):
        """GET, and then POST, both return OK"""

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/', {'id': self.id})
        self.assertEqual(response.status_code, 200)

    def test_getpost2(self):
        """GET, and then POST, and then POST, all return OK"""

        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/', {'id': self.id})
        self.assertEqual(response.status_code, 200)
        response = self.client.post('/', {'id': self.id})
        self.assertEqual(response.status_code, 200)
