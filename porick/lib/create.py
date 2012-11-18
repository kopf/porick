import bcrypt
import re
from sqlalchemy import or_

from pylons import tmpl_context as c

import porick.lib.helpers as h
from porick.model import db, Quote, User

def create_quote(quote_body, notes, tags):
    newquote = Quote()
    newquote.body = quote_body
    newquote.notes = notes
    newquote.tags = [h.create_or_get_tag(tag) for tag in tags]
    newquote.submitted_by = c.user
    
    db.add(newquote)
    db.commit()
    return True


def create_user(username, password, email):
    conflicts = db.query(User).filter(or_(User.email == email,
                                          User.username == username)).first()
    if conflicts:
        if conflicts.email == email:
            raise NameError('Sorry! That email already exists in the system.')
        elif conflicts.username == username:
            raise NameError('Sorry! That username is already taken.')
    
    hashed_pass = h.hash_password(password)
    new_user = User()
    new_user.username = username
    new_user.password = hashed_pass
    new_user.email = email
    
    db.add(new_user)
    db.commit()
    return True


def validate_signup(username, password, password_confirm, email):
    valid_password = validate_password(password, password_confirm)
    if not valid_password['status']:
        return valid_password
        
    if not (username and password and password_confirm and email):
        return {'status': False,
                'msg': 'Please fill in all the required fields.'}

    email_regex = re.compile('''[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-zA-Z0-9!#$%'''
                             '''&'*+/=?^_`{|}~-]+)*@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]*'''
                             '''[a-zA-Z0-9])?\.)+[a-zA-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?''')
    if not email_regex.match(email):
        return {'status': False,
                'msg': 'Please enter a valid email address.'}

    username_regex = re.compile('''^[a-zA-Z0-9_]*$''')
    if not username_regex.match(username):
        return {'status': False,
                'msg': 'Your username may consist only of'
                       ' alphanumeric characters and underscores.'}

    return {'status': True}

def validate_password(password, password_confirm):
    if not len(password) >= 8:
        return {'status': False,
                'msg': 'Your password must be at least 8 characters long.'}

    if not password == password_confirm:
        return {'status': False,
                'msg': 'Your password did not match in both fields.'}
    return {'status': True}