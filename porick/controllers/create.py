import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

import porick.lib.helpers as h
from porick.lib.base import BaseController, render
from porick.model.model import Quote, QuoteToTag
from porick.model.meta import Session as db

log = logging.getLogger(__name__)

class CreateController(BaseController):

    def quote(self):
        c.page = 'new quote'
        if request.environ['REQUEST_METHOD'] == 'GET':
            return render('/create/quote/form.mako')
        elif request.environ['REQUEST_METHOD'] == 'POST':
            quote_body = request.params['quote_body']
            if not quote_body:
                abort(400)
            tags = request.params['tags'].split(' ')
            notes = request.params['notes'] or u''
            newquote = Quote()
            newquote.body = quote_body
            newquote.notes = notes
            newquote.tags = [h.create_or_get_tag(tag) for tag in tags]
            
            db.add(newquote)
            db.commit()

            return render('/create/quote/success.mako')

        else:
            abort(400)

    def user(self):
        c.page = "sign up"
        if request.environ['REQUEST_METHOD'] == 'GET':
            return render('/create/user/form.mako')
        elif request.environ['REQUEST_METHOD'] == 'POST':
            abort(404)
