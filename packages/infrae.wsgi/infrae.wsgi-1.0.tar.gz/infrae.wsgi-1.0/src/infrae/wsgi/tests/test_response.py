# Copyright (c) 2010 Infrae. All rights reserved.
# See also LICENSE.txt
# $Id: test_response.py 43374 2010-07-08 10:30:02Z sylvain $

from infrae.wsgi.response import WSGIResponse
from infrae.wsgi.tests.mockers import MockWSGIStartResponse

import unittest


class ResponseTestCase(unittest.TestCase):

    def setUp(self):
        self.start_response = MockWSGIStartResponse()

    def test_simple(self):
        """Test a simple reply.
        """
        response = WSGIResponse({}, self.start_response)
        response.setBody('<p>Hello</p>')
        response.startWSGIResponse()

        self.assertEqual(self.start_response.status, '200 OK')
        self.assertEqual(
            self.start_response.headers,
            [('Content-Length', '12'),
             ('Content-Type', 'text/html;charset=utf-8')])
        self.assertEqual(self.start_response.data, [])

    def test_status(self):
        """Test setting/getting a status.
        """
        response = WSGIResponse({}, self.start_response)
        self.assertEqual(response.getStatus(), 200)
        response.setStatus(404)
        self.assertEqual(response.getStatus(), 404)
        response.setBody('<p>Not found</p>')
        response.startWSGIResponse()

        self.assertEqual(self.start_response.status, '404 Not Found')
        self.assertEqual(
            self.start_response.headers,
            [('Content-Length', '16'),
             ('Content-Type', 'text/html;charset=utf-8')])
        self.assertEqual(self.start_response.data, [])

    def test_write(self):
        """Test using the write method of Request object.
        """
        response = WSGIResponse({}, self.start_response)
        response.write('Hello')
        response.write('World')
        response.startWSGIResponse()

        self.assertEqual(self.start_response.status, '200 OK')
        self.assertEqual(
            self.start_response.headers,
            [('Content-Type', 'text/html;charset=utf-8')])
        self.assertEqual(self.start_response.data, ['Hello', 'World'])

    def test_headers(self):
        """Try to set some headers.
        """
        response = WSGIResponse({}, self.start_response)
        response.setHeader('cache-control', 'max-age=1200')
        response.addHeader('x-downloaded', 42)
        self.assertEqual(response.getHeader('X-Downloaded'), 42)
        self.assertEqual(response.getHeader('Cache-control'), 'max-age=1200')
        response.setBody('<p>News</p>')
        response.startWSGIResponse()

        self.assertEqual(self.start_response.status, '200 OK')
        self.assertEqual(
            self.start_response.headers,
            [('Cache-Control', 'max-age=1200'),
             ('Content-Length', '11'),
             ('Content-Type', 'text/html;charset=utf-8'),
             ('X-Downloaded', '42')])
        self.assertEqual(self.start_response.data, [])

    def test_content_type_and_length(self):
        """Here we set a custom content-type and length.
        """
        response = WSGIResponse({}, self.start_response)
        response.setHeader('content-type', 'text/csv')
        self.assertEqual(response.getHeader('Content-Type'), 'text/csv')
        response.setHeader('content-length', 1024)
        response.setBody('blue;yellow')
        response.startWSGIResponse()

        self.assertEqual(self.start_response.status, '200 OK')
        self.assertEqual(
            self.start_response.headers,
            [('Content-Length', '1024'),
             ('Content-Type', 'text/csv')])
        self.assertEqual(self.start_response.data, [])

    def test_content_type_and_length_with_write(self):
        """We here set the content type and length before streaming
        using the write method.
        """
        response = WSGIResponse({}, self.start_response)
        response.setHeader('content-type', 'text/csv')
        self.assertEqual(response.getHeader('Content-Type'), 'text/csv')
        response.setHeader('content-length', 1024)
        response.write('blue;yellow')
        response.write('green;black')
        response.startWSGIResponse()

        self.assertEqual(self.start_response.status, '200 OK')
        self.assertEqual(
            self.start_response.headers,
            [('Content-Length', '1024'),
             ('Content-Type', 'text/csv')])
        self.assertEqual(
            self.start_response.data, ['blue;yellow', 'green;black'])

    def test_redirect(self):
        """Test redirect to a URL.
        """
        response = WSGIResponse({}, self.start_response)
        response.redirect('http://infrae.com')
        response.setBody('<p>Redirect to Infrae</p>')
        self.assertEqual(response.getStatus(), 302)
        response.startWSGIResponse()

        self.assertEqual(self.start_response.status, '302 Moved Temporarily')
        self.assertEqual(
            self.start_response.headers,
            [('Content-Length', '25'),
             ('Content-Type', 'text/html;charset=utf-8'),
             ('Location', 'http://infrae.com')])
        self.assertEqual(self.start_response.data, [])

    def test_redirect_with_status(self):
        """Test redirect to a URL providing a status.
        """
        response = WSGIResponse({}, self.start_response)
        response.redirect('http://infrae.com', status=301)
        self.assertEqual(response.getStatus(), 301)
        response.setBody('<p>Redirect to Infrae</p>')
        response.startWSGIResponse()

        self.assertEqual(self.start_response.status, '301 Moved Permanently')
        self.assertEqual(
            self.start_response.headers,
            [('Content-Length', '25'),
             ('Content-Type', 'text/html;charset=utf-8'),
             ('Location', 'http://infrae.com')])
        self.assertEqual(self.start_response.data, [])

    def test_redirect_no_content(self):
        """Test redirect without setting any content.
        """
        response = WSGIResponse({}, self.start_response)
        response.redirect('http://infrae.com')
        self.assertEqual(response.getStatus(), 302)
        response.startWSGIResponse()

        self.assertEqual(self.start_response.status, '302 Moved Temporarily')
        self.assertEqual(
            self.start_response.headers,
            [('Content-Length', '0'),
             ('Location', 'http://infrae.com')])
        self.assertEqual(self.start_response.data, [])

    def test_cookies(self):
        """Try to set a cookie.
        """
        response = WSGIResponse({}, self.start_response)
        response.setCookie('Silva', 'Best CMS Ever')
        response.setBody('<p>Silva</p>')
        response.startWSGIResponse()

        self.assertEqual(self.start_response.status, '200 OK')
        self.assertEqual(
            self.start_response.headers,
            [('Content-Length', '12'),
             ('Content-Type', 'text/html;charset=utf-8'),
             ('Set-Cookie', 'Silva="Best%20CMS%20Ever"')])
        self.assertEqual(self.start_response.data, [])

    def test_cookies_expire(self):
        """Expire a cookie.
        """
        response = WSGIResponse({}, self.start_response)
        response.setCookie('Silva', 'Best CMS Ever')
        response.expireCookie('Silva')
        response.setBody('<p>Silva</p>')
        response.startWSGIResponse()

        self.assertEqual(self.start_response.status, '200 OK')
        self.assertEqual(
            self.start_response.headers,
            [('Content-Length', '12'),
             ('Content-Type', 'text/html;charset=utf-8'),
             ('Set-Cookie', 'Silva="deleted"; Max-Age=0; Expires=Wed, 31-Dec-97 23:59:59 GMT')])
        self.assertEqual(self.start_response.data, [])

    def test_cookies_multiples(self):
        """Set more than one cookie.
        """
        response = WSGIResponse({}, self.start_response)
        response.setCookie('Silva', 'Best CMS Ever')
        response.setCookie('WSGI', 'Pluggable')
        response.setBody('<p>Silva</p>')
        response.startWSGIResponse()

        self.assertEqual(self.start_response.status, '200 OK')
        self.assertEqual(
            self.start_response.headers,
            [('Content-Length', '12'),
             ('Content-Type', 'text/html;charset=utf-8'),
             ('Set-Cookie', 'Silva="Best%20CMS%20Ever"'),
             ('Set-Cookie', 'WSGI="Pluggable"')])
        self.assertEqual(self.start_response.data, [])

    def test_cookies_append(self):
        """Append a value at the end of a cookie.
        """
        response = WSGIResponse({}, self.start_response)
        response.setCookie('Silva', 'Best CMS Ever')
        response.appendCookie('Silva', 'Soon in 3D')
        response.setBody('<p>Silva</p>')
        response.startWSGIResponse()

        self.assertEqual(self.start_response.status, '200 OK')
        self.assertEqual(
            self.start_response.headers,
            [('Content-Length', '12'),
             ('Content-Type', 'text/html;charset=utf-8'),
             ('Set-Cookie', 'Silva="Best%20CMS%20Ever%3ASoon%20in%203D"')])
        self.assertEqual(self.start_response.data, [])

def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ResponseTestCase))
    return suite
