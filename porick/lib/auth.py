import bcrypt
import hashlib

from pylons import response, request, url
from pylons import tmpl_context as c
from pylons.controllers.util import redirect

import porick.lib.helpers as h
from porick.model import db, User
from porick.settings import COOKIE_SECRET, PASSWORD_SALT


def authenticate(username, password):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if bcrypt.hashpw(password, PASSWORD_SALT) == user.password:
        set_auth_cookie(user)
        return True
    return False


def authorize():
    if not c.logged_in:
        redirect(url(controller='account', action='login', redirect_url=url.current(), warn='true'))


def set_auth_cookie(user):
    auth = hashlib.md5('%s:%s' % (COOKIE_SECRET,
                                  user.username)).hexdigest()
    response.set_cookie('auth', auth, max_age=3600) 
    response.set_cookie('username', user.username, max_age=3600)


def clear_cookies():
    response.delete_cookie('auth')
    response.delete_cookie('username')
