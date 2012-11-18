import logging
import datetime

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from pylons.decorators import jsonify

from porick.lib.auth import authorize
from porick.lib.base import BaseController, render
import porick.lib.helpers as h
from porick.model import (db, QSTATUS, Quote, VoteToUser, 
                          ReportedQuotes, DeletedQuotes, now)

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
                return {'msg': 'Invalid quote ID.',
                        'status': 'error'}
            quote.status = QSTATUS['approved']
            db.commit()
            return {'msg': 'Quote approved.',
                    'status': 'success'}
        else:
            abort(405)

    @jsonify
    def delete(self, quote_id):
        if request.environ['REQUEST_METHOD'] == 'DELETE':
            delete_check = self._is_deleteable_or_disapprovable(quote_id)
            if delete_check['status'] == 'error':
                return delete_check
            else:
                quote = delete_check['quote']
            quote.status = QSTATUS['deleted']
            msg = 'Quote deleted.'
            db.commit()
            return {'msg': msg,
                    'status': 'success'}
        else:
            abort(405)

    @jsonify
    def disapprove(self, quote_id):
        if request.environ['REQUEST_METHOD'] == 'POST':
            delete_check = self._is_deleteable_or_disapprovable(quote_id)
            if delete_check['status'] == 'error':
                return delete_check
            else:
                quote = delete_check['quote']
            quote.status = QSTATUS['disapproved']
            msg = 'Quote disapproved.'
            db.commit()
            return {'msg': msg,
                    'status': 'success'}
        else:
            abort(405)

    @jsonify
    def favourite(self, quote_id):
        authorize()
        quote = db.query(Quote).filter(Quote.id == quote_id).first()
        if not quote:
            return {'msg': 'Invalid quote ID.',
                    'status': 'error'}
        if request.environ['REQUEST_METHOD'] == 'POST':
            c.user.favourites.append(quote)
            db.commit()
            return {'msg': 'Quote favourited.',
                    'status': 'success'}
        elif request.environ['REQUEST_METHOD'] == 'DELETE':
            if not quote in c.user.favourites:
                return {'msg': "Can't remove: This quote isn't in your favourites.",
                        'status': 'error'}
            c.user.favourites.remove(quote)
            db.commit()
            return {'msg': 'Removed favourite.',
                    'status': 'success'}
        else:
            abort(405)
    
    @jsonify
    def report(self, quote_id):
        authorize()
        quote = db.query(Quote).filter(Quote.id == quote_id).first()
        if not quote:
            return {'msg': 'Invalid quote ID.',
                    'status': 'error'}
        if request.environ['REQUEST_METHOD'] == 'POST':
            if self._has_made_too_many_reports():
                # TODO: This should return a HTTP 429! But pylons.controllers.util.abort()
                #       doesn't seem to support it :/
                return {'msg': 'You are reporting quotes too fast. Slow down!',
                        'status': 'error'}
            if db.query(ReportedQuotes).filter_by(user_id=c.user.id).\
                filter_by(quote_id=quote.id).first():
                return {'msg': 'You already reported this quote in the past. Ignored.',
                        'status': 'error'}
            if not quote.status == QSTATUS['approved']:
                return {'msg': 'Quote is not approved, therefore cannot be reported.',
                        'status': 'error'}
            if db.query(ReportedQuotes).filter_by(user_id=c.user.id).\
                filter_by(quote_id=quote.id).first():
                return {'msg': 'You already reported this quote in the past. Ignored.',
                        'status': 'error'}
            c.user.reported_quotes.append(quote)
            quote.status = QSTATUS['reported']
            db.commit()
            
            return {'msg': 'Quote reported.',
                    'status': 'success'}
        else:
            abort(405)

    @jsonify
    def vote(self, quote_id, direction):
        authorize()
        quote = db.query(Quote).filter(Quote.id == quote_id).first()
        if request.environ['REQUEST_METHOD'] == 'POST':
            if not quote:
                return {'msg': 'Invalid quote ID.',
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
                return {'msg': 'Invalid vote direction.',
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
                return {'msg': 'Invalid vote direction.',
                        'status': 'error'}
            
            quote.votes -= 1
            db.commit()
            return {'status': 'success',
                    'msg': 'Vote annulled!'}
        else:
            abort(405)

    def _has_made_too_many_reports(self):
        # TODO:
        # This filtering / counting should be done by SQLAlchemy.
        #
        # This is a quick hack to get around problems with between() and filter/filter_by,
        # possibly caused by the fact that ReportedQuotes is a Table() obj and not a class
        #
        reports = db.query(ReportedQuotes).filter_by(user_id=c.user.id).all()
        limit = 5
        limit_time = now() - datetime.timedelta(hours=1)
        i = 0
        found = []
        for report in reports:
            if limit_time < report.time:
                found.append(report)
            if i == limit:
                break
            i += 1
        return len(found) >= limit

    def _is_deleteable_or_disapprovable(self, quote_id):
        authorize()
        quote = db.query(Quote).filter(Quote.id == quote_id).first()
        if not quote:
            return {'msg': 'Invalid quote ID.',
                    'status': 'error'}
        if not h.quote_is_deleteable(quote):
            return {'msg': 'You do not have permission to delete this quote.',
                    'status': 'error'}
        c.user.deleted_quotes.append(quote)
        return {'status': 'success', 'quote': quote}