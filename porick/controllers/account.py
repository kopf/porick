import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from porick.lib.auth import authenticate, clear_cookies
from porick.lib.base import BaseController, render
from porick.lib.create import create_user, validate_signup
import porick.lib.helpers as h

log = logging.getLogger(__name__)

class AccountController(BaseController):

    def create(self):
        c.page = 'sign up'
        if request.environ['REQUEST_METHOD'] == 'GET':
            return render('/signup/form.mako')
        elif request.environ['REQUEST_METHOD'] == 'POST':
            username = request.params['username']
            password = request.params['password']
            password_confirm = request.params['password_confirm']
            email = request.params['email']
            
            validity = validate_signup(username, password,
                                       password_confirm, email)
            if not validity['status']:
                h.add_message(validity['msg'], 'error')
                return render('/signup/form.mako')
            try:
                create_user(username, password, email)
                authenticate(username, password)
                self._process_auth_cookies()
                return render('/signup/success.mako')
            except NameError, e:
                h.add_message(e.__str__, 'error')
                return render('/signup/form.mako')

    def login(self):
        c.page = 'login'
        c.redirect_url = request.GET.get('redirect_url', '')
        if request.environ['REQUEST_METHOD'] == 'GET':
            if request.GET.get('warn', ''):
                h.add_message('You need to be logged in to perform that action.',
                              'info')
            return render('/login.mako')
        elif request.environ['REQUEST_METHOD'] == 'POST':
            username = request.params['username']
            password = request.params['password']
            success = authenticate(username, password)
            if success:
                if c.redirect_url and not c.redirect_url == '/signup':
                    redirect(c.redirect_url)
                else:
                    redirect(url(controller='home', action='main'))
            else:
                h.add_message('Incorrect username / password', 'error')
                return render('/login.mako')

    def logout(self):
        c.page = 'logout'
        clear_cookies()
        c.logged_in = False
        h.add_message('Logged out successfully!', 'info')
        return render('/home.mako')
