from porick.tests import *

class TestVoteController(TestController):

    def test_index(self):
        response = self.app.get(url(controller='vote', action='index'))
        # Test response...
