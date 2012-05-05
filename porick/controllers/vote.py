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
    def vote(self):
        if request.environ['REQUEST_METHOD'] != 'POST':
            abort(405)
        try:
            quote_id = request.params['quote_id']
            direction = request.params['direction']
        except KeyError:
            abort(400)

        quote = db.query(Quote).filter(Quote.id == quote_id)
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
        return {'status': 'success',
                'msg': 'Vote cast!'}
