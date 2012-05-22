import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from porick.lib.auth import authorize
from porick.lib.base import BaseController, render
import porick.lib.helpers as h
from porick.model import db, QSTATUS, Quote, VoteToUser

log = logging.getLogger(__name__)

class ApiV1Controller(BaseController):

    @jsonify
    def approve(self, quote_id):
        authorize()
        if not h.is_admin():
            abort(401)
        if request.environ['REQUEST_METHOD'] == 'POST':
            quote = db.query(Quote).filter(Quote.id == quote_id).first()
            if not quote:
                return {'msg': 'Invalid quote ID',
                        'status': 'error'}
            quote.status = QSTATUS['approved']
            db.commit()
            return {'msg': 'Quote approved',
                    'status': 'success'}

    @jsonify
    def favourite(self, quote_id):
        authorize()
        quote = db.query(Quote).filter(Quote.id == quote_id).first()
        if not quote:
            return {'msg': 'Invalid quote ID',
                    'status': 'error'}
        if request.environ['REQUEST_METHOD'] == 'PUT':
            c.user.favourites.append(quote)
            db.commit()
            return {'msg': 'Quote favourited',
                    'status': 'success'}
        elif request.environ['REQUEST_METHOD'] == 'DELETE':
            if not quote in c.user.favourites:
                return {'msg': "Can't remove: This quote isn't in your favourites",
                        'status': 'error'}
            c.user.favourites.remove(quote)
            db.commit()
            return {'msg': 'Removed favourite',
                    'status': 'success'}

    @jsonify
    def report(self, quote_id):
        authorize()
        quote = db.query(Quote).filter(Quote.id == quote_id).first()
        if not quote:
            return {'msg': 'Invalid quote ID',
                    'status': 'error'}
        if request.environ['REQUEST_METHOD'] == 'PUT':
            if not quote.status == QSTATUS['approved']:
                return {'msg': 'Quote is not approved, therefore cannot be reported',
                        'status': 'error'}
            c.user.reported_quotes.append(quote)
            quote.status = QSTATUS['reported']
            db.commit()
            return {'msg': 'Quote reported',
                    'status': 'success'}

    @jsonify
    def vote(self, direction, quote_id):
        authorize()
        quote = db.query(Quote).filter(Quote.id == quote_id).first()
        if request.environ['REQUEST_METHOD'] == 'PUT':
            if not quote:
                return {'msg': 'Invalid quote ID',
                        'status': 'error'}

            already_voted = ''
            for assoc in quote.voters:
                if assoc.user == c.user:
                    already_voted = True
                    # cancel the last vote:
                    if assoc.direction == 'up':
                        quote.rating -= 1
                    elif assoc.direction == 'down':
                        quote.rating += 1
                    db.delete(assoc)
            
            assoc = VoteToUser(direction=direction)
            assoc.user = c.user
            quote.voters.append(assoc)

            if direction == 'up':
                quote.rating += 1
            elif direction == 'down':
                quote.rating -= 1
            else:
                return {'msg': 'Invalid vote direction',
                        'status': 'error'}

            if not already_voted:
                quote.votes += 1
            db.commit()
            return {'status': 'success',
                    'msg': 'Vote cast!'}
        elif request.environ['REQUEST_METHOD'] == 'DELETE':
            for assoc in quote.voters:
                if assoc.user == c.user:
                    db.delete(assoc)
            if direction == 'up':
                quote.rating -= 1
            elif direction == 'down':
                quote.rating += 1
            else:
                return {'msg': 'Invalid vote direction',
                        'status': 'error'}
            
            quote.votes -= 1
            db.commit()
            return {'status': 'success',
                    'msg': 'Vote annulled!!'}

        else:
            abort(405)
