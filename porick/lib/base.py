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
        c.logged_in = False
        c.username = ''
        c.page = ''
        c.messages = []

        auth = request.cookies.get('auth')
        username = request.cookies.get('username')
        if auth:
            if hashlib.md5('%s:%s' % (COOKIE_SECRET, username)).hexdigest() == auth:
                c.logged_in = True
                c.username = username
        
