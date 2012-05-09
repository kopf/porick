"""The base Controller API

Provides the BaseController class for subclassing.
"""
import hashlib

from pylons import request
from pylons import tmpl_context as c
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render

from porick.model.meta import Session
from porick.settings import COOKIE_SECRET

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            Session.remove()

    def __before__(self, action, **params):
        self._set_auth_cookies()

    def _set_auth_cookies(self):
        c.logged_in = False
        c.username = ''
        c.page = ''
        c.user_level = 0
        c.messages = []

        auth = request.cookies.get('auth')
        username = request.cookies.get('username')
        level = request.cookies.get('level')
        if auth:
            if hashlib.md5('%s:%s:%s' % (COOKIE_SECRET, username, level)).hexdigest() == auth:
                c.logged_in = True
                c.username = username
                c.user_level = int(level)
        
