# vim: set expandtab ts=4 sw=4 filetype=python:

import abc
import logging

from rattlesnake.response import Response

log = logging.getLogger('rattlesnake.handlers')

class Handler(object):

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def wants_to_handle(self, request):
        """
        Subclasses must define me!
        """

    @abc.abstractmethod
    def handle(self, request):
        """
        Subclasses must define me!
        """

class NotFound(Handler):

    def wants_to_handle(self, request):
        return self

    def handle(self, request):

        return Response(
            '404 Not Found',
            [('Content-Type', 'text/plain')],
            ['Sorry, no handlers are specified for %s'
                % request.pretty_request])

class ItWorks(Handler):

    def wants_to_handle(self, request):

         if request.is_GET and request.PATH_INFO == '/does-it-work':
            return self

    def handle(self, request):
        return Response.plain(['it works'])
