import cgi

from pylons import tmpl_context as c
from paste.urlparser import PkgResourcesParser
from pylons.middleware import error_document_template
from webhelpers.html.builder import literal

from porick.lib.base import BaseController, render

class ErrorController(BaseController):
    """Generates error documents as and when they are required.

    The ErrorDocuments middleware forwards to ErrorController when error
    related status codes are returned from the application.

    This behaviour can be altered by changing the parameters to the
    ErrorDocuments middleware in your config/middleware.py file.

    """
    def document(self):
        """Render the error document"""
        request = self._py_object.request
        resp = request.environ.get('pylons.original_response')
        code = cgi.escape(request.GET.get('code', ''))
        content = cgi.escape(request.GET.get('message', ''))
        if resp:
            content = literal(resp.status)
            code = code or cgi.escape(str(resp.status_int))
        if not code:
            raise Exception('No status code was found')
        c.code = code
        c.message = content
        c.page = None
        return render('/error.mako')
