# -*- coding: utf-8 -*-

from webob import Response, Request
from khan.utils.decorator import *
from khan.utils.testing import *

class OneInvalidResponseFilter(InvalidResponseFilter):
    def __call__(self, resp, invalid):
        resp.headers['item'] = 0
        return resp

class TwoInvalidResponseFilter(InvalidResponseFilter):
    def __call__(self, resp, invalid):
        resp.headers['item'] = resp.headers['item'] + 1
        return resp

class ThreeInvalidResponseFilter(InvalidResponseFilter):
    def __call__(self, resp, invalid):
        resp.headers['item'] = str(resp.headers['item'] + 1)
        resp.body = 'value'
        return resp

def mydecorator(on_invalid):
    def decorator(handler):
        def newfunc(req):
            return on_invalid(req, InvalidException("request restricted"))
        return update_wrapper_for_handler(newfunc, handler)
    return decorator

class TestInvalidHandler(TestCase):
    
    def test_basic(self):
        req = Request.blank("/")
        handler = lambda req : Response("aaa")
        new_handler = mydecorator(HTTPStatusOnInvalid(200) | \
           OneInvalidResponseFilter() | \
           TwoInvalidResponseFilter() | \
           ThreeInvalidResponseFilter())(handler)
        resp = new_handler(req)
        self.assertEqual('200 OK', resp.status, 'response status must be 200')
        self.assertEqual('value', resp.body, resp.body)
        self.assertEqual('2', resp.headers['item'], 'response headers item == 2')
        
    def test_RedirectOnInvalid(self):
        req = Request.blank("/")
        handler = lambda req : Response("aaa")
        new_handler = mydecorator(RedirectOnInvalid('/index'))(handler)
        resp = new_handler(req)
        self.assertEqual(302, resp.status_int)
        self.assertTrue(resp.location.endswith("/index"))
    
    def test_HTTPStatusOnInvalid(self):
        req = Request.blank("/")
        handler = lambda req : Response("aaa")
        new_handler = mydecorator(HTTPStatusOnInvalid(404))(handler)
        resp = new_handler(req)
        self.assertEqual(404, resp.status_int)
    
    def test_RedirectFilter(self):
        req = Request.blank("/")
        handler = lambda req : Response("aaa")
        new_handler = mydecorator(HTTPStatusOnInvalid(404) | RedirectFilter("/index"))(handler)
        resp = new_handler(req)
        self.assertEqual(302, resp.status_int)
        self.assertTrue(resp.location.endswith("/index"))
        