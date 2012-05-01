import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from porick.lib.base import BaseController, render
from porick.settings import SITE_NAME, WELCOME_TEXT, HOMEPAGE_BUTTON_TEXT

log = logging.getLogger(__name__)

class HomeController(BaseController):

    def main(self):
        c.site_name = SITE_NAME
        c.welcome_text = WELCOME_TEXT
        c.button_text = HOMEPAGE_BUTTON_TEXT
        return render('/home.mako')
