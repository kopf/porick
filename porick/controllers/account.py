import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from porick.lib.auth import authenticate, clear_cookies
from porick.lib.base import BaseController, render
from porick.lib.create import create_user
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
            email = request.params['email']
            if not (username and password and email):
                abort(400)
            try:
                create_user(username, password, email)
                return render('/signup/success.mako')
            except NameError, e:
                h.add_message(e.__str__, error)
                return render('/signup/form.mako')

    def login(self):
        c.page = 'login'
        c.redirect_url = request.GET.get('redirect_url', '')
        if request.environ['REQUEST_METHOD'] == 'GET':
            if c.redirect_url:
                h.add_message('You need to be logged in to perform that action.',
                              'info')
            return render('/login.mako')
        elif request.environ['REQUEST_METHOD'] == 'POST':
            username = request.params['username']
            password = request.params['password']
            success = authenticate(username, password)
            if success:
                if c.redirect_url:
                    redirect(c.redirect_url)
                else:
                    redirect(url(controller='home', action='main'))
            else:
                h.add_message('Incorrect username / password', 'error')
                return render('/login.mako')

    def logout(self):
        clear_cookies()
        h.add_message('Logged out successfully!', 'info')
        return render('/base.mako')
