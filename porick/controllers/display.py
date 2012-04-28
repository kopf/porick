import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from porick.lib.base import BaseController, render
from porick.model.model import Quote
from porick.model.meta import Session as db


log = logging.getLogger(__name__)


class DisplayController(BaseController):

    def index(self):
        retval = ''
        for row in db.query(Quote).all():
            retval += row.body
        return retval
