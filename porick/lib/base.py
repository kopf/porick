"""The base Controller API

Provides the BaseController class for subclassing.
"""
import hashlib
import routes

from pylons import request, config
from pylons import tmpl_context as c
from pylons.controllers import WSGIController
from pylons.templating import render_mako as render

from porick.model import User
from porick.model.meta import Session as db

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            db.remove()

    def __before__(self, action, **params):
        self._fix_routes()
        self._set_context_var_defaults()
        self._process_auth_cookies()

    def _fix_routes(self):
        env = {}
        for k,v in request.environ.items():
            env[k]=v
        env['SCRIPT_NAME'] = ''
        config = routes.request_config()
        config.environ = env

    def _set_context_var_defaults(self):
        c.page = ''
        c.paginator = None
        c.quote = None
        c.messages = []

    def _process_auth_cookies(self):
        c.logged_in = False
        c.user = None

        auth = request.cookies.get('auth')
        username = request.cookies.get('username')
        level = request.cookies.get('level')
        if auth:
            if hashlib.md5('%s:%s:%s' % (config['COOKIE_SECRET'], username, level)).hexdigest() == auth:
                c.user = db.query(User).filter(User.username == username).first()
                if c.user:
                    c.logged_in = True
        
