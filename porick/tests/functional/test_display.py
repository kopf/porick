from porick.tests import *

class TestDisplayController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='display', action='index'))
        # Test response...
