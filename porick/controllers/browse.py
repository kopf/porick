import math
import logging
import sqlalchemy as sql

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from porick.lib.base import BaseController, render
from porick.model.model import Quote, QuoteToTag, Tag
from porick.model.meta import Session as db
from porick.settings import QUOTES_PER_PAGE

log = logging.getLogger(__name__)


class BrowseController(BaseController):

    def main(self):
        c.quotes = db.query(Quote).order_by(Quote.submitted.desc()).filter(Quote.approved == 1).limit(QUOTES_PER_PAGE)
        c.page = 'browse'
        return render('/browse.mako')

    def best(self):
        c.quotes = db.query(Quote).order_by(Quote.score.desc()).filter(Quote.approved == 1).limit(QUOTES_PER_PAGE)
        c.page = 'best'
        return render('/browse.mako')

    def worst(self):
        c.quotes = db.query(Quote).order_by(Quote.score).filter(Quote.approved == 1).limit(QUOTES_PER_PAGE)
        c.page = 'worst'
        return render('/browse.mako')

    def random(self):
        c.quotes = [db.query(Quote).order_by(sql.func.rand()).filter(Quote.approved == 1).first()]
        c.page = 'random'
        return render('/browse.mako')

    def tags(self, tag=None):
        if tag is None:
            c.rainbow = False
            if 'rainbow' in request.params:
                c.rainbow = ['', 'label-success', 'label-warning', 
                             'label-important', 'label-info', 'label-inverse']

            c.tags = self._generate_tagcloud()
            c.page = 'tags'
            return render('/tagcloud.mako')
        else:
            tag_obj = db.query(Tag).filter(Tag.tag == tag).first()
            c.quotes = db.query(Quote).filter(Quote.tags.contains(tag_obj)).all()
            c.page = 'tags'
            c.tag_filter = tag
            return render('/browse.mako')

    def view_one(self, ref_id):
        quote = db.query(Quote).filter(Quote.id == ref_id).first()
        if not quote or quote.approved != 1:
            abort(404)
        else:
            c.quotes = [quote]
            c.tags = self._get_tags_for_quotes(c.quotes)
            c.page = 'browse'
            return render('/browse.mako')

    def _generate_tagcloud(self):
        retval = {}
        for tag in db.query(Tag).all():
            count = db.query(QuoteToTag).filter_by(tag_id=tag.id).count()
            retval[tag.tag] = count or 1
            retval[tag.tag] = math.log(retval[tag.tag], math.e/2)
        return retval
