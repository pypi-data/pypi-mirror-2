# -*- coding: utf-8 -*-

import unittest
from webob.exc import status_map
from webob import Response
from khan.utils.testing import *
from khan.httpstatus import HTTPStatus, HTTPStatusDispatcher

class TestHTTPStatus(TestCase):
    
    def test(self):
        self.assertTrue(HTTPStatus(404), Response)
        app = TestApp(HTTPStatus(404, detail = "text"))
        self.assertTrue("text" in app.get("/", status = "*").body)
        for code, cls in status_map.items():
            if code in [304, 204]:
                continue 
            def wsgi_app(environ, start_response):
                resp = HTTPStatus(code)
                return resp(environ, start_response)
            test_app = TestApp(wsgi_app)
            resp = test_app.get("/", status = "*")
            self.assertTrue(resp.status_int == code)
            
class TestHTTPStatusDispatcherMiddleware(TestCase):
    
    def test_basic(self):
        app = HTTPStatusDispatcher(lambda environ, start_response : HTTPStatus(404)(environ, start_response))
        # handle 404 的 app 将返回 500
        app[404] = lambda environ, start_response : HTTPStatus(500)(environ, start_response)
        res = TestApp(app).get("/", status = "*")
        # 因为 HTTPStatusDispatcher 的 keep_response 被设置为 True， 那么状态码应该仍然为 404, 而不是 500
        assert res.status_int == 404
        
        app = HTTPStatusDispatcher(lambda environ, start_response : HTTPStatus(404)(environ, start_response), False)
        # handle 404 的 app 将返回 500
        app[404] = lambda environ, start_response : HTTPStatus(500)(environ, start_response)
        res = TestApp(app).get("/", status = "*")
        # 因为 HTTPStatusDispatcher 的 keep_response 被设置为 False， 那么状态码应该仍然为 500, 而不是 404
        assert res.status_int == 500
        
        # 返回 200 的 app
        app = HTTPStatusDispatcher(lambda environ, start_response : HTTPStatus(200)(environ, start_response), False)
        # handle 404 的 app 将返回 500
        app[404] = lambda environ, start_response : HTTPStatus(500)(environ, start_response)
        res = TestApp(app).get("/", status = "*")
        # 因为未捕获到匹配的状态码，所以仍然返回原始 app 的状态
        assert res.status_int == 200

if __name__ == "__main__":
    unittest.main()
   