import datetime
import logging
import string
import random

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

from porick.lib.auth import authenticate, clear_cookies
from porick.lib.base import BaseController, render
from porick.lib.create import create_user, validate_signup, validate_password
from porick.lib.mail import send_reset_password_email
from porick.model import now, db, User, PasswordResets
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
                                                             '/logout',
                                                             '/reset_password']:
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
        c.key = request.params.get('key')
        c.redirect_url = url(controller='account', action='login')
        if request.environ['REQUEST_METHOD'] == 'GET':
            if not c.key:
                return render('/pw_reset/request.mako')
            else:
                reset_token = self._check_valid_pw_reset_key(c.key)
                if not reset_token:
                    h.add_message('Invalid reset token', 'error')
                    return render('/blank.mako')
                return render('/pw_reset/set.mako')
        elif request.environ['REQUEST_METHOD'] == 'POST':
            if not c.key:
                # create a password request key
                email = request.params['email']
                user = db.query(User).filter(User.email == email).first()
                if not user:
                    h.add_message('Invalid email address provided.', 'error')
                    return render('/pw_reset/request.mako')
                already_requested = db.query(PasswordResets).filter(PasswordResets.user_id == user.id).first()
                if already_requested:
                    if already_requested.created < now() - datetime.timedelta(hours=2):
                        db.delete(already_requested)
                    else:
                        h.add_message('A password reset has already been requested for this user.', 'error')
                        return render('/blank.mako')
                pw_reset_key = PasswordResets()
                pw_reset_key.user_id = user.id
                pw_reset_key.key = self._generate_pw_reset_key()
                db.add(pw_reset_key)
                db.commit()

                send_reset_password_email(user.email, pw_reset_key.key)
                h.add_message('Password reset email sent!', 'success')
                return render('/blank.mako')
            else:
                # reset the user's password to what they've submitted
                reset_token = self._check_valid_pw_reset_key(c.key)
                if not reset_token:
                    h.add_message('Invalid reset token', 'error')
                    return render('/blank.mako')
                password = request.params['password']
                password_confirm = request.params['password_confirm']
                valid_password = validate_password(password, password_confirm)
                if not valid_password['status']:
                    h.add_message(valid_password['msg'], 'error')
                    return render('/pw_reset/set.mako')
                user = db.query(User).filter(User.id == reset_token.user_id).first()
                hashed_pass = h.hash_password(password)
                user.password = hashed_pass
                db.delete(reset_token)
                db.commit()

                h.add_message('Password successfully set. You should now be able to login.', 'success')
                return render('/blank.mako')


    def _check_valid_pw_reset_key(self, key):
        reset_token = db.query(PasswordResets).filter(PasswordResets.key == key).first()
        if not reset_token:
            return None
        elif reset_token.created < now() - datetime.timedelta(hours=2):
            db.delete(reset_token)
            return None
        return reset_token

    def _generate_pw_reset_key(self):
        chars = string.ascii_letters + string.digits
        valid = False
        key = ''
        while not valid:
            key = ''.join(random.choice(chars) for _ in range(26))
            already_exists = db.query(PasswordResets).filter(PasswordResets.key == key).first()
            if not already_exists:
                valid = True
        return key