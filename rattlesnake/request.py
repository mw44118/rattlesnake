# vim: set expandtab ts=4 sw=4 filetype=python:

import collections
import Cookie
import logging
import urlparse

log = logging.getLogger('rattlesnake.request')

class Request(collections.MutableMapping):

    """
    Wraps up the environ dictionary in an object with lots of cute
    properties.

    But if you want to pretend the request IS the environ dictionary,
    you can.
    """

    def __init__(self, dbconn, config_wrapper, environ):
        self.dbconn = dbconn
        self.config_wrapper = config_wrapper
        self.environ = environ

    @property
    def HTTP_COOKIE(self):
        return self.get('HTTP_COOKIE')

    @property
    def PATH_INFO(self):
        return self.get('PATH_INFO')

    @property
    def REQUEST_METHOD(self):
        return self.get('REQUEST_METHOD')

    @property
    def QUERY_STRING(self):
        return self.get('QUERY_STRING')

    @property
    def is_GET(self):
        return self.get('REQUEST_METHOD') == 'GET'

    @property
    def is_POST(self):
        return self.get('REQUEST_METHOD') == 'POST'

    @property
    def parsed_QS(self):

        if self.QUERY_STRING:
            return urlparse.parse_qs(self.QUERY_STRING)

        else:
            return {}

    @property
    def parsed_facebook_cookie(self):

        if 'parsed_facebook_cookie' in self:
            return self['parsed_facebook_cookie']

        elif self.parsed_cookie:

            k = 'fbs_%s' % self.config_wrapper.facebook_app_id

            if k not in self.parsed_cookie:
                return

            # The facebook SDK expects the cookie to be a dictionary that
            # maps fbs_... to the string.
            cookie_dict = {k:self.parsed_cookie[k].value}

            parsed_facebook_cookie = facebook.get_user_from_cookie(
                cookie_dict,
                str(self.config_wrapper.facebook_app_id),
                self.config_wrapper.facebook_app_secret)

            self['parsed_facebook_cookie'] = parsed_facebook_cookie

            return parsed_facebook_cookie

        else:
            self['parsed_facebook_cookie'] = None


    @property
    def facebook_uid(self):

        if 'facebook_uid' in self:
            return self['facebook_uid']

        elif self.parsed_facebook_cookie:

            self['facebook_uid'] = self.parsed_facebook_cookie['uid']
            return self.parsed_facebook_cookie['uid']

        else:
            self['facebook_uid'] = None


    @property
    def parsed_cookie(self):

        if 'rattlesnake.parsed_cookie' in self:
            return self['rattlesnake.parsed_cookie']

        if self.HTTP_COOKIE:
            c = Cookie.SimpleCookie()
            c.load(self.HTTP_COOKIE)
            self['rattlesnake.parsed_cookie'] = c
            return c

    @property
    def body(self):

        """
        Read everything from the request body and store it under the key
        'request.body'.

        Don't use this if you suspect you might get a POST that's so big
        that you can't load it all into memory.
        """

        if 'request.body' in self:
            return self['request.body']

        else:
            self['request.body'] = self.read_request_body()
            return self['request.body']


    def read_request_body(self):

        if 'wsgi.input' in self and 'CONTENT_LENGTH' in self:
            return self['wsgi.input'].read(int(self['CONTENT_LENGTH']))

    @property
    def parsed_body(self):

        if self.body:
            return urlparse.parse_qs(self.body)

    # These magic methods allow the Request object to act like a
    # dictionary.
    def __getitem__(self, k):
        return self.environ[k]

    def __delitem__(self, k):
        return self.environ.__delitem__(k)

    def __setitem__(self, k, v):
        self.environ[k] = v

    def __iter__(self):
        return iter(self.environ)

    def __len__(self):
        return len(self.environ)
