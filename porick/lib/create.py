import bcrypt
from sqlalchemy import or_

import porick.lib.helpers as h
from porick.model import db, Quote, User
from porick.settings import PASSWORD_SALT

def create_quote(quote_body, notes, tags):
    try:
        newquote = Quote()
        newquote.body = quote_body
        newquote.notes = notes
        newquote.tags = [h.create_or_get_tag(tag) for tag in tags]
        
        db.add(newquote)
        db.commit()
    except Exception, e:
        # TODO: add proper exception handling
        return False
    return True


def create_user(username, password, email):
    conflicts = db.query(User).filter(or_(User.email == email,
                                          User.username == username)).first()
    if conflicts:
        if conflicts.email == email:
            raise NameError('Sorry! That email already exists in the system.')
        elif conflicts.username == username:
            raise NameError('Sorry! That username is already taken.')
    
    hashed_pass = bcrypt.hashpw(password, PASSWORD_SALT)
    new_user = User()
    new_user.username = username
    new_user.password = hashed_pass
    new_user.email = email
    
    db.add(new_user)
    db.commit()
    return True
    
