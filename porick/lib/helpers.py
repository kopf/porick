import random

from webhelpers.html import literal
from pylons import url

from porick.model.model import Quote, Tag
from porick.model.meta import Session as db

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
