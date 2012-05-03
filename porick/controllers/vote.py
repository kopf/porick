import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from porick.lib.base import BaseController, render

log = logging.getLogger(__name__)

class VoteController(BaseController):

    def vote(self):
        if request.environ['REQUEST_METHOD'] != 'POST':
            abort(405)
        try:
            quote_id = request.params['quote_id']
            direction = request.params['direction']
        except KeyError:
            abort(400)
