import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from porick.lib.auth import authenticate, clear_cookies
from porick.lib.base import BaseController, render
from porick.lib.create import create_user, validate_signup
from porick.model import db, User
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
                c.logged_in = True
                c.user = db.query(User).filter(User.username == username).first()
                return render('/signup/success.mako')
            except NameError, e:
                h.add_message(e.__str__(), 'error')
                return render('/signup/form.mako')

    def login(self):
        c.page = 'log in'
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
                if c.redirect_url and not c.redirect_url in ['/signup', 
                                                             '/logout']:
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

    def reset_password(self):
        c.page = 'pw reset'
        c.redirect_url = url(controller='account', action='login')
        if request.environ['REQUEST_METHOD'] == 'GET':
            return render('/reset_password.mako')
        elif request.environ['REQUEST_METHOD'] == 'POST':
            email = request.params['email']
            user = db.query(User).filter(User.email == email).first()
            if not user:
                h.add_message('Invalid email address provided.', 'error')
                return render('/reset_password.mako')
            new_password = h.generate_password()
            user.password = h.hash_password(new_password)
            db.commit()
            
            h.add_message('Password reset email sent!', 'success')
            return render('/reset_password.mako')