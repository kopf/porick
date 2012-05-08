import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from porick.lib.auth import authenticate
from porick.lib.base import BaseController, render
from porick.lib.create import create_user

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
                c.error = e.__str__
                return render('/signup/error.mako')

    def login(self):
        c.page = 'login'
        if request.environ['REQUEST_METHOD'] == 'GET':
            return render('/login/form.mako')
        elif request.environ['REQUEST_METHOD'] == 'POST':
            username = request.params['username']
            password = request.params['password']
            success = authenticate(username, password)
            if success:
                redirect(url(controller='home', action='main'))
            else:
                c.error = 'Incorrect username / password'
                return render('/login/error.mako')
