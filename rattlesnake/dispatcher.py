# vim: set expandtab ts=4 sw=4 filetype=python:

import logging
import sys

from rattlesnake.request import Request
from rattlesnake.handlers import NotFound

log = logging.getLogger('rattlesnake.dispatcher')

class Dispatcher(object):

    """
    This is the webapp that your WSGI server (gunicorn) talks to.
    """

    def __init__(self):
        self.setup_handlers()

    def setup_handlers(self):
        self.handlers = [NotFound()]

    def __call__(self, environ, start_response):

        """
        Every time a request hits the WSGI server, this function gets
        called.

        Put startup stuff in the __init__, not in here!
        """

        try:

            req = Request(environ)

            if req.QUERY_STRING:

                log.debug('Dispatching %(REQUEST_METHOD)s '
                    '%(PATH_INFO)s?%(QUERY_STRING)s' % req)

            else:

                log.debug('Dispatching %(REQUEST_METHOD)s %(PATH_INFO)s'
                    % req)

            h = self.find_handler(req)

            log.debug('Sending request to %s.' % h.__class__.__name__)

            resp = h.handle(req)

            start_response(resp.status, resp.headers)

            log.debug('Replying with status %s.' % resp.status)

            return resp.body

        except Exception, ex:

            log.critical(environ)
            log.exception(ex)

            start_response(
                '500 ERROR',
                [('Content-Type', 'text/plain')],
                sys.exc_info())

            return [
                """Sorry, something went wrong internally.  """
                """It's not you, it's me."""]


    def find_handler(self, request):

        """
        Return the first handler that wants to handle this request.
        """

        for h in self.handlers:
            if h.wants_to_handle(request):
                return h
