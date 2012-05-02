import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

import porick.lib.helpers as h
from porick.lib.base import BaseController, render
from porick.model.model import Quote, QuoteToTag
from porick.model.meta import Session as db

log = logging.getLogger(__name__)

class CreateController(BaseController):

    def main(self):
        if request.environ['REQUEST_METHOD'] == 'GET':
            return render('/create/main.mako')
        elif request.environ['REQUEST_METHOD'] == 'POST':
            quote_body = request.params['quote_body']
            if not quote_body:
                abort(400)
            tags = request.params['tags'].split(' ')
            notes = request.params['notes'] or u''
            tag_ids = []
            for tag in tags:
                newtag = h.create_or_get_tag(tag)
                tag_ids.append(newtag.id)
            newquote = Quote()
            newquote.body = quote_body
            newquote.notes = notes
            
            db.add(newquote)
            db.commit()

            for tag_id in tag_ids:
                mapping = QuoteToTag()
                mapping.quote_id = newquote.id
                mapping.tag_id = tag_id
                db.add(mapping)

            db.commit()
            return render('/create/success.mako')

        else:
            abort(400)

