import bcrypt
import hashlib

from pylons import response, request

from porick.model.model import User
from porick.model.meta import Session as db
from porick.settings import COOKIE_SECRET, PASSWORD_SALT


def authenticate(username, password):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if bcrypt.hashpw(password, PASSWORD_SALT) == user.password:
        set_auth_cookie(user)
        return True
    return False


def set_auth_cookie(user):
    auth = hashlib.md5('%s:%s' % (COOKIE_SECRET,
                                  user.username)).hexdigest()
    response.set_cookie('auth', auth, max_age=3600) 
    response.set_cookie('username', user.username, max_age=3600)


def clear_cookies():
    request.cookies.pop('auth', None)
    request.cookies.pop('username', None)
