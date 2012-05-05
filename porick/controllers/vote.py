import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from porick.lib.base import BaseController, render
from porick.model.model import Quote
from porick.model.meta import Session as db

log = logging.getLogger(__name__)

class VoteController(BaseController):

    @jsonify
    def vote(self, direction, quote_id):
        if request.environ['REQUEST_METHOD'] not in ['PUT', 'DELETE']:
            abort(405)

        quote = db.query(Quote).filter(Quote.id == quote_id).first()
        if not quote:
            return {'msg': 'Invalid quote ID',
                    'status': 'error'}

        if direction == 'up':
            quote.rating += 1
        elif direction == 'down':
            quote.rating -= 1
        else:
            return {'msg': 'Invalid vote direction',
                    'status': 'error'}

        quote.votes += 1
        db.commit()
        return {'status': 'success',
                'msg': 'Vote cast!'}
