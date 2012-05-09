import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from porick.lib.base import BaseController, render

log = logging.getLogger(__name__)

class HomeController(BaseController):

    def main(self):
        c.page = 'home'
        return render('/home.mako')
