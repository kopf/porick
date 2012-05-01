from porick.tests import *

class TestCreateController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='create', action='index'))
        # Test response...
