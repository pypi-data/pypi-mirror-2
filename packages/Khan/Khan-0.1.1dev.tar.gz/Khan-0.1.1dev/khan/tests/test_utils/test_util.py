# -*- coding: utf-8 -*-

import os
from paste.httpexceptions import HTTPExceptionHandler
from webob import Request, Response
from khan.utils.testing import *
from khan.utils import *
from khan.httpstatus import HTTPStatus

class TestUtils(TestCase):

    def test_redirect_to_0(self):

        def App(environ, start_response):
            if environ['PATH_INFO'].startswith("/not_found"):
                redirect_to("/yet_not_found", status_code = 404)
            elif environ['PATH_INFO'].startswith('/default'):
                redirect_to("/yet_default")

            return HTTPStatus(200)(environ, start_response)

        app = TestApp(HTTPExceptionHandler(App))
        app.get('/not_found', status=404)
        app.get('/default', status=302)        

    def test_redirect_to_01(self):

        full_path = None

        def App(environ, start_response):

            assert full_path == construct_path(environ), "full path error"

            return HTTPStatus(200)(environ, start_response)

        app = TestApp(HTTPExceptionHandler(App))
        full_path = '/not_found'
        app.get(full_path)
        full_path = '/default'
        app.get(full_path)
        
        
    def test_redirect_to_02(self):

        def App(environ, start_response):
            
            return HTTPStatus(200)(environ, start_response)

        app = TestApp(HTTPExceptionHandler(App))
        full_path = '/not_found'
        app.get(full_path)
        full_path = '/default'
        app.get(full_path)
        
    def test_request_classifier(self):

        def App(environ, start_response):

            obj = request_classifier(environ)
            self.assertTrue(obj in requestTypes, 'request_classifier 返回对象不再 ReqestTypes 范围')

            return HTTPStatus(200)(environ, start_response)

        app = TestApp(App)
        app.get('/')

        # empty will raise a error
        def empty_dict_raise():
            request_classifier({})
        self.assertRaises(ValueError, empty_dict_raise)
        # not dict raise a error
        def not_dict_raise():
            request_classifier(None)
        self.assertRaises(ValueError, not_dict_raise)

    def test_dispatch_on(self):
        
        def dispatch_handler_get(environ, start_response):
            return HTTPStatus(302)(environ, start_response)
        
        def dispatch_handler_post(environ, start_response):
            return HTTPStatus(301)(environ, start_response)

        @dispatch_on(
            get = dispatch_handler_get,
            post = dispatch_handler_post
        )
        def App(environ, start_response):
            return HTTPStatus(200)(environ, start_response)

        app = TestApp(App)
        self.assertTrue(app.get('/').status_int == 302, 'status_code errror')
        self.assertTrue(app.post('/').status_int == 301, 'status_code errror')
        self.assertTrue(app.put('/').status_int == 200, 'status_code errror')

    def test_construct_path(self):

        def App(environ, start_response):
            method = environ['REQUEST_METHOD'].lower()
            if method == 'get':
                self.assertTrue(construct_path(environ) == '/long/get/long/', 'post full path lost')
            elif method == 'post':
                self.assertTrue(construct_path(environ) == '/long/post/long/', 'post full path lost')
            elif method == 'put':
                self.assertTrue(construct_path(environ) == '/long/put/long/', 'post full path lost')
            
            return HTTPStatus(200)(environ, start_response)

        app = TestApp(App)
        app.get('/long/get/long/')
        app.post('/long/post/long/')
        app.put('/long/put/long/')

    def test_aswsgi(self):

        @aswsgi
        def webob_app(req):
            return HTTPStatus(200)

        app = TestApp(webob_app)
        self.assertTrue(app.get('/').status_int == 200, 'aswsgi error')

    def test_ashandler(self):
        
        @ashandler
        def App(environ, start_response):
            start_response("200 OK", [("content-type", "plain/text")])
            return ["body"]

        req = Request.blank('/')
        resp = App(req)
        self.assertTrue(resp.status_int == 200, 'ashandler error')
    
    def test_abort(self):

        def App(environ, start_response):
            if environ['PATH_INFO'].startswith("/not_found"):
                abort(404, "Not Found")
            elif environ['PATH_INFO'].startswith('/abort_default'):
                abort(500)

            return HTTPStatus(200)(environ, start_response)

        app = TestApp(HTTPExceptionHandler(App))
        app.get('/not_found', status=404)
        app.get('/abort_default', status=500)
    
    def test_asresponse(self):
        
        def app(environ, start_response):
            start_response("200 OK", [("content-type", "plain/text")])
            return ["body"]
        
        resp = AsResponse(app)
        self.assertTrue(isinstance(resp, Response), "`AsResponse` is not `webob.Response`")
        app = TestApp(resp)
        self.failUnlessEqual(app.get("/").body, "body")

    def test_singleton(self):
        
        class MySingleton(Singleton): pass
        
        a = MySingleton()
        b = MySingleton()
        self.assertEqual(a, b)
    
    def test_isiterable(self):
        self.assertTrue(isiterable([]))
        self.assertTrue(isiterable((1,2,)))
        self.assertTrue(isiterable({}))
        self.assertTrue(not isiterable("str"))
    
    def test_unique_id(self):
        self.assertTrue(unique_id() != unique_id())
    
    def test_classid(self):
        class C(object): pass
        self.assertEqual(type(classid(C)), str)
        
if __name__ == "__main__":
    unittest.main()
