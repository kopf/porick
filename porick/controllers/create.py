import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from porick.lib.base import BaseController, render

log = logging.getLogger(__name__)

class CreateController(BaseController):

    def main(self):
        if request.environ['REQUEST_METHOD'] == 'GET':
            return render('/create.mako')
        elif request.environ['REQUEST_METHOD'] == 'POST':
            quote_body = request.params['quote_body']
            if not quote_body:
                abort(400)
            tags = request.params['tags'].split(' ')
            notes = request.params['notes']
            return "quote_body: %s\ntags: %s\nnotes: %s" % (quote_body, tags, notes)
        else:
            abort(400)

