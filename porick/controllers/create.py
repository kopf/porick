import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

import porick.lib.helpers as h
from porick.lib.auth import authorize
from porick.lib.base import BaseController, render
from porick.lib.create import create_quote, create_user


log = logging.getLogger(__name__)

class CreateController(BaseController):

    def quote(self):
        authorize()
        c.page = 'new quote'
        if request.environ['REQUEST_METHOD'] == 'GET':
            return render('/create/form.mako')
        elif request.environ['REQUEST_METHOD'] == 'POST':
            quote_body = request.params.get('quote_body', '')
            if not quote_body:
                abort(400)
            notes = request.params.get('notes', '')
            tags = filter(None, request.params.get('tags', '').replace(',', ' ').split(' '))

            
            result = create_quote(quote_body, notes, tags)
            if result:
                return render('/create/success.mako')
            else:
                abort(500)
        else:
            abort(400)

