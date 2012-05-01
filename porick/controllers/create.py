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
            abort(500)
        else:
            abort(400)

