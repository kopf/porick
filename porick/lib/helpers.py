import random

from webhelpers.html import literal
from pylons import url
from pylons import tmpl_context as c

from porick.model import db, Quote, Tag, User

def cgi_unescape(s):
    s = s.replace('&quot;', '"')
    s = s.replace('&gt;', '>')
    s = s.replace('&lt;', '<')
    s = s.replace('&amp;', '&')
    return s

def create_or_get_tag(tagname):
    tag = db.query(Tag).filter(Tag.tag == tagname).first()
    if not tag:
        tag = Tag()
        tag.tag = tagname
        db.add(tag)
        db.commit()
    return tag

def get_score_mouseover(quote, direction):
    if direction == 'up':
        count = quote.votes
    else:
        count = quote.votes - quote.rating
    retval = '%s %svote' % (count, direction)
    if count != 1:
        retval += 's'
    return retval

def add_message(msg, level):
    c.messages.append({'msg': msg, 'level': level})

def check_if_voted(quote):
    if not c.logged_in:
        return False
    for assoc in quote.voters:
        if assoc.user.username == c.user.username:
            return assoc.direction

def is_admin():
    return c.logged_in and c.user.level == 1

def show_approval_button():
    return c.page in ['unapproved', 'reported'] and is_admin()

def quote_is_deleteable(quote):
    if not c.logged_in:
        return False
    else:
        return quote.submitted_by == c.user or c.user.level == 1