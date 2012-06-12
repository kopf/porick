import math
import logging
import sqlalchemy as sql

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
import webhelpers.paginate as paginate

from porick.lib.auth import authorize
from porick.lib.base import BaseController, render
import porick.lib.helpers as h
from porick.model import db, QSTATUS, Quote, QuoteToTag, Tag

log = logging.getLogger(__name__)


class BrowseController(BaseController):

    def main(self, page=1):
        quotes = db.query(Quote).order_by(Quote.submitted.desc()).filter(Quote.status == QSTATUS['approved']).all()
        c.paginator = self._create_paginator(quotes, page)
        c.page = 'browse'
        return render('/browse.mako')

    def best(self, page=1):
        quotes = db.query(Quote).order_by(Quote.rating.desc()).filter(Quote.status == QSTATUS['approved']).all()
        c.paginator = self._create_paginator(quotes, page)
        c.page = 'best'
        return render('/browse.mako')

    def worst(self, page=1):
        quotes = db.query(Quote).order_by(Quote.rating).filter(Quote.status == QSTATUS['approved']).all()
        c.paginator = self._create_paginator(quotes, page)
        c.page = 'worst'
        return render('/browse.mako')

    def random(self):
        c.quote = db.query(Quote).order_by(sql.func.rand()).filter(Quote.status == QSTATUS['approved']).first()
        c.page = 'random'
        return render('/browse.mako')

    def search(self, keyword='', page=1):
        if request.environ['REQUEST_METHOD'] == 'POST':
            keyword = request.params.get('keyword', '')
            redirect(url(controller='browse', action='search', keyword=keyword))
        query = '%' + keyword + '%'
        quotes = db.query(Quote).filter(Quote.body.like(query)).filter(Quote.status == QSTATUS['approved']).order_by(Quote.submitted.desc()).all()
        c.paginator = self._create_paginator(quotes, page)
        c.page = 'search: %s' % keyword
        return render('/browse.mako')
        

    def tags(self, tag=None, page=1):
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
            quotes = db.query(Quote).filter(Quote.tags.contains(tag_obj)).filter(Quote.status == QSTATUS['approved']).all()
            c.paginator = self._create_paginator(quotes, page)
            c.tag_filter = tag
            return render('/browse.mako')

    def view_one(self, ref_id):
        quote = db.query(Quote).filter(Quote.id == ref_id).first()
        if not quote or quote.status != QSTATUS['approved']:
            abort(404)
        else:
            c.quote = quote
            c.page = 'browse'
            return render('/browse.mako')

    def disapproved(self, page=1):
        if not c.logged_in:
            h.add_message('You must be logged in to perform that action.', 'error')
            return render('/blank.mako')
        quotes = db.query(Quote).filter(Quote.status == QSTATUS['disapproved']).order_by(Quote.submitted.desc()).all()
        c.paginator = self._create_paginator(quotes, page)
        c.page = 'disapproved'
        return render('/browse.mako')

    def unapproved(self, page=1):
        if not h.is_admin():
            h.add_message('You must be an admin to perform that action.', 'error')
            return render('/blank.mako')
        quotes = db.query(Quote).filter(Quote.status == QSTATUS['unapproved']).order_by(Quote.submitted.desc()).all()
        c.paginator = self._create_paginator(quotes, page)
        c.page = 'unapproved'
        return render('/browse.mako')

    def reported(self, page=1):
        if not h.is_admin():
            h.add_message('You must be an admin to perform that action.', 'error')
            return render('/blank.mako')
        quotes = db.query(Quote).filter(Quote.status == QSTATUS['reported']).all()
        c.paginator = self._create_paginator(quotes, page)
        c.page = 'reported'
        return render('/browse.mako')

    def deleted(self, page=1):
        if not h.is_admin():
            h.add_message('You must be an admin to perform that action.', 'error')
            return render('/blank.mako')
        quotes = db.query(Quote).filter(Quote.status == QSTATUS['deleted']).all()
        c.paginator = self._create_paginator(quotes, page)
        c.page = 'deleted'
        return render('/browse.mako')

    def favourites(self, page=1):
        authorize()
        c.paginator = self._create_paginator(c.user.favourites, page)
        c.page = 'favourites'
        return render('/browse.mako')

    def _generate_tagcloud(self):
        retval = {}
        for tag in db.query(Tag).all():
            count = db.query(QuoteToTag).filter_by(tag_id=tag.id).count()
            retval[tag.tag] = count or 1
            retval[tag.tag] = math.log(retval[tag.tag], math.e/2)
        return retval

    def _create_paginator(self, quotes, page):
        return paginate.Page(quotes, page=page, items_per_page=10)
