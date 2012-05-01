import logging
import sqlalchemy as sql

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from porick.lib.base import BaseController, render
from porick.model.model import Quote
from porick.model.meta import Session as db
from porick.settings import QUOTES_PER_PAGE

log = logging.getLogger(__name__)


class BrowseController(BaseController):

    def main(self):
        c.quotes = db.query(Quote).order_by(Quote.submitted.desc()).limit(QUOTES_PER_PAGE).all()
        return render('/browse.mako')

    def best(self):
        c.quotes = db.query(Quote).order_by(Quote.score.desc()).limit(QUOTES_PER_PAGE).all()
        return render('/browse.mako')

    def worst(self):
        c.quotes = db.query(Quote).order_by(Quote.score).limit(QUOTES_PER_PAGE).all()
        return render('/browse.mako')

    def random(self):
        c.quotes = [db.query(Quote).order_by(sql.func.rand()).first()]
        return render('/browse.mako')

    def tags(self):
        abort(404)

    def view_one(self, ref_id):
        quote = db.query(Quote).filter(Quote.id == ref_id).first()
        if not quote:
            abort(404)
        else:
            c.quotes = [quote]
            return render('/browse.mako')
