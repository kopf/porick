import logging

from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect

import porick.lib.helpers as h
from porick.lib.base import BaseController, render
from porick.lib.create import create_quote, create_user


log = logging.getLogger(__name__)

class CreateController(BaseController):

    def quote(self):
        c.page = 'new quote'
        if request.environ['REQUEST_METHOD'] == 'GET':
            return render('/create/quote/form.mako')
        elif request.environ['REQUEST_METHOD'] == 'POST':
            quote_body = request.params['quote_body']
            if not quote_body:
                abort(400)
            notes = request.params['notes'] or u''
            tags = request.params['tags'].split(' ')
            
            result = create_quote(quote_body, notes, tags)
            if result:
                return render('/create/quote/success.mako')
            else:
                abort(500)
        else:
            abort(400)

    def user(self):
        c.page = "sign up"
        if request.environ['REQUEST_METHOD'] == 'GET':
            return render('/create/user/form.mako')
        elif request.environ['REQUEST_METHOD'] == 'POST':
            username = request.params['username']
            password = request.params['password']
            email = request.params['email']
            if not username or password or email:
                abort(400)
            try:
                result = create_user(username, password, email)
            except NameError, e:
                c.error = e.__str__
                return render('/create/user/error.mako')
