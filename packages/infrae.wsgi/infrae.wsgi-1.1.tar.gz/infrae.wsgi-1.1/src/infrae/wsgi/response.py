# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id: response.py 44707 2010-08-23 17:22:04Z sylvain $

from ZPublisher.HTTPResponse import status_reasons
from ZPublisher.Iterators import IStreamIterator
from ZPublisher.pubevents import PubBeforeStreaming
from zope.publisher.interfaces.http import IResult
from zope.event import notify
import zExceptions

from infrae.wsgi.headers import HTTPHeaders

from urllib import quote
import socket


class AbortPublication(Exception):
    """Exception to abort all the publication process.
    """

    def __init__(self, started=True):
        self.response_started = started


class StreamIteratorIterator(object):
    """Make a IStreamIterator a real iterator, because it lack of an
    __iter__ method ...
    """

    def __init__(self, stream):
        assert IStreamIterator.providedBy(stream)
        self.__stream = stream

    def __iter__(self):
        return self.__stream


def format_cookies(cookies):
    """Format cookies as WSGI HTTP headers.
    """
    formatted_cookies = []
    for name, options in cookies.items():
        cookie = '%s="%s"' % (name, quote(options['value']))
        for key, value in options.items():
            key = key.lower()
            if key == 'expires':
                cookie = '%s; Expires=%s' % (cookie, value)
            elif key == 'domain':
                cookie = '%s; Domain=%s' % (cookie, value)
            elif key == 'path':
                cookie = '%s; Path=%s' % (cookie, value)
            elif key == 'max_age':
                cookie = '%s; Max-Age=%s' % (cookie, value)
            elif key == 'comment':
                cookie = '%s; Comment=%s' % (cookie, value)
            elif key == 'secure' and value:
                cookie = '%s; Secure' % cookie
            # Some browsers recognize this cookie attribute
            # and block read/write access via JavaScript
            elif key == 'http_only' and value:
                cookie = '%s; HTTPOnly' % cookie
        formatted_cookies.append(('Set-Cookie', cookie))
    return formatted_cookies


class WSGIResponse(object):
    """A response object using a WSGI connection

    This Response object knows nothing about ZServer, but tries to be
    compatible with the ZPublisher.HTTPResponse.
    """
    default_charset = 'utf-8'
    realm = 'Zope'

    # This is just need by FSDTMLFile. It should be removed when no
    # DTML files a re needed anymore
    __allow_access_to_unprotected_subobjects__ = 1

    def __init__(self, environ, start_response, debug_mode=False):
        self.headers = HTTPHeaders()
        self.status = 200
        self.cookies = {}
        self.body = None
        self.debug_mode = debug_mode
        self.__environ = environ
        self.__start_response = start_response
        self.__started = False
        self.__write = None

    def redirect(self, location, status=302):
        self.status = status
        self.headers['Location'] = location

    def write(self, data):
        # This is deprecated, please return an iterable instead of
        # using write()
        if self.__write is None:
            self.__write = self.startWSGIResponse(stream=True)
        try:
            if isinstance(data, unicode):
                data = data.encode(self.default_charset)
            self.__write(data)
        except (socket.error, IOError):
            # If we can't write anymore to the socket, abort all the
            # publication process.
            raise AbortPublication(started=True)

    def setBase(self, base):
        # HTTPResponse compatibility dumb
        pass

    def setBody(self, body, **options):
        # We ignore options
        if isinstance(body, unicode):
            body = body.encode(self.default_charset)
        self.body = body

    def setStatus(self, status, msg=None):
        # We ignore msg and use our own.
        self.status = status

    def getStatus(self):
        return self.status

    def setHeader(self, name, value, literal=0):
        # literal=0 is for HTTPResponse compatibility
        self.headers[name] = value

    addHeader = setHeader

    def getHeader(self, name, literal=0):
        # literal=0 is for HTTPResponse compatibility
        return self.headers.get(name)

    def appendCookie(self, name, value):
        name = str(name)
        value = str(value)

        cookies = self.cookies
        if cookies.has_key(name):
            cookie = cookies[name]
        else:
            cookie = cookies[name] = {}
        if cookie.has_key('value'):
            cookie['value'] = '%s:%s' % (cookie['value'], value)
        else:
            cookie['value'] = value

    def expireCookie(self, name, **options):
        options['max_age'] = 0
        options['expires'] = 'Wed, 31-Dec-97 23:59:59 GMT'
        self.setCookie(name, 'deleted', **options)

    def setCookie(self, name, value, **options):
        name = str(name)
        value = str(value)

        cookies = self.cookies
        if cookies.has_key(name):
            cookie = cookies[name]
        else:
            cookie = cookies[name] = {}
        for cookie_key, cookie_value in options.items():
            cookie[cookie_key] = cookie_value
        cookie['value'] = value

    def startWSGIResponse(self, stream=False):
        if self.__started:
            return self.__write
        self.__started = True

        # If the body is an IResult, it is a case of streaming where
        # we don't fix headers.
        stream = stream or IResult.providedBy(self.body)

        if not stream:
            # If we are not streaming, we try to set Content-Length,
            # Content-Type and adapt status if there is no content.
            if not self.headers.has_key('Content-Length'):
                content_length = None
                if isinstance(self.body, str) or \
                        isinstance(self.body, unicode) or \
                        IStreamIterator.providedBy(self.body):
                    content_length = len(self.body)
                elif self.body is None:
                    content_length = 0
                if content_length is not None:
                    self.headers['Content-Length'] = content_length

            if self.headers.has_key('Content-Length'):
                content_length = self.headers['Content-Length']
                if not content_length and self.status == 200:
                    # Set no content status if there is no content
                    self.status = 204

            if not self.headers.has_key('Content-Type'):
                if content_length:
                    # If there is content and no Content-Type, set HTML
                    self.headers['Content-Type'] = 'text/html;charset=%s' % (
                        self.default_charset,)
        else:
            # Fire event before streaming
            notify(PubBeforeStreaming(self))

            # Fix default Content-Type
            if not self.headers.has_key('Content-Type'):
                self.headers['Content-Type'] = 'text/html;charset=%s' % (
                    self.default_charset,)


        formatted_status = "%d %s" % (
            self.status, status_reasons.get(self.status, 'OK'))
        formatted_headers = self.headers.items() + format_cookies(self.cookies)
        return self.__start_response(formatted_status, formatted_headers)

    def getWSGIResponse(self):
        # This return a tuple (data_sent, data_to_send_to_WSGI)
        result = self.body
        if result is not None:
            # If we have an iterator, we say that data have been sent
            # in order not to commit the transaction finish consuming
            # the iterator.
            if IStreamIterator.providedBy(result):
                return (True, StreamIteratorIterator(result))
            elif IResult.providedBy(result):
                return (True, result)
            return (self.__started, [result,])
        return (self.__started, [])

    def _unauthorized(self):
        # Unauthorized is implemented like this to be compliant with PAS
        self.setHeader(
            'WWW-Authenticate', 'basic realm="%s"' % self.realm)

    # ZPublisher define a method for each error on the response
    # object. We need to add them to be compatible

    def unauthorized(self):
        raise zExceptions.Unauthorized("Please authenticate")

    def debugError(self, name):
        raise zExceptions.NotFound(name)

    def forbiddenError(self, name):
        raise zExceptions.Forbidden(name)

    def badRequestError(self, name):
        raise zExceptions.BadRequest(name)

    def notFoundError(self, name):
        raise zExceptions.NotFound(name)

    # Support for ConflictError/Retry. We reuse the same response.

    def retry(self):
        return self
