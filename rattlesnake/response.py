# vim: set expandtab ts=4 sw=4 filetype=python:

import logging

log = logging.getLogger('rattlesnake.response')

class Response(object):

    def __init__(self, status, headers, body):
        self.status = status
        self.headers = headers
        self.body = body

    @property
    def http_status(self):

        """
        You say tomah-to, I say tomay-to.
        """

        return self.status

    @classmethod
    def RedirectResponse(cls, location):
        """
        Return a 302 redirect response.
        """

        return cls('302 FOUND', [('Location', location)], [])

    redirect = RedirectResponse

    @classmethod
    def html(cls, body):

        """
        Return a 200 OK response with HTML content.
        """

        return cls(
            '200 OK',
            [('Content-Type', 'text/html; charset=utf-8')],
            body)

    def update_session(self, session):

        """
        Add a Set-Cookie header to the response, based on data in the
        session object.
        """

        self.headers.extend(session.wsgi_headers)

    @classmethod
    def plain(cls, body):
        return cls('200 OK', [('Content-Type', 'text/plain')], body)
