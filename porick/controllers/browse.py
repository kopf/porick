import math
import logging
import sqlalchemy as sql

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from porick.lib.base import BaseController, render
from porick.model import db, Quote, QuoteToTag, Tag

log = logging.getLogger(__name__)


class BrowseController(BaseController):

    def main(self):
        c.quotes = db.query(Quote).order_by(Quote.submitted.desc()).filter(Quote.approved == 1).limit(10)
        c.page = 'browse'
        return render(self._get_template_name())

    def best(self):
        c.quotes = db.query(Quote).order_by(Quote.score.desc()).filter(Quote.approved == 1).limit(10)
        c.page = 'best'
        return render(self._get_template_name())

    def worst(self):
        c.quotes = db.query(Quote).order_by(Quote.score).filter(Quote.approved == 1).limit(10)
        c.page = 'worst'
        return render(self._get_template_name())

    def random(self):
        c.quotes = [db.query(Quote).order_by(sql.func.rand()).filter(Quote.approved == 1).first()]
        c.page = 'random'
        return render(self._get_template_name())

    def search(self):
        if request.environ['REQUEST_METHOD'] != 'POST':
            # TOTO:
            # return an advanced search page, but in the meantime:
            abort(405)
        else:
            keyword = request.params.get('keyword', '')
            query = '%' + keyword + '%'
            c.quotes = db.query(Quote).order_by(Quote.submitted.desc()).filter(Quote.body.like(query)).limit(10)
            c.page = 'search: %s' % keyword
            return render(self._get_template_name())
        

    def tags(self, tag=None):
        c.page = 'tags'
        if tag is None:
            c.rainbow = False
            if 'rainbow' in request.params:
                c.rainbow = ['', 'label-success', 'label-warning', 
                             'label-important', 'label-info', 'label-inverse']

            c.tags = self._generate_tagcloud()
            return render('/tagcloud.mako')
        else:
            tag_obj = db.query(Tag).filter(Tag.tag == tag).first()
            c.quotes = db.query(Quote).filter(Quote.tags.contains(tag_obj)).limit(10)
            c.tag_filter = tag
            return render(self._get_template_name())

    def view_one(self, ref_id):
        quote = db.query(Quote).filter(Quote.id == ref_id).first()
        if not quote or quote.approved != 1:
            abort(404)
        else:
            c.quotes = [quote]
            c.tags = self._get_tags_for_quotes(c.quotes)
            c.page = 'browse'
            return render(self._get_template_name())

    def _generate_tagcloud(self):
        retval = {}
        for tag in db.query(Tag).all():
            count = db.query(QuoteToTag).filter_by(tag_id=tag.id).count()
            retval[tag.tag] = count or 1
            retval[tag.tag] = math.log(retval[tag.tag], math.e/2)
        return retval

    def _get_template_name(self):
        return '/browse-logged_in.mako' if c.logged_in else '/browse.mako'
