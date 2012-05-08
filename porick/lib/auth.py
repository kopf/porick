import bcrypt
import hashlib

from pylons import response

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
    value = hashlib.md5('%s:%s:%s' % (COOKIE_SECRET,
                                      user.username,
                                      user.level)).hexdigest()
    response.set_cookie('auth', value, max_age=3600) 
