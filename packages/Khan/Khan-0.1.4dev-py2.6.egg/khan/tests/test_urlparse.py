# -*- coding: utf-8 -*-

from webob import Response
from khan.utils.testing import *
from khan.urlparse import *

class TestFilterDispatcher(TestCase):
    
    def print_pathinfo(self, environ, start_response):
        return Response(environ.get("PATH_INFO", ""))(environ, start_response)

    def jpg_filter(self, app):
        def filter_jpg(environ, start_response):
            environ["khan.test.jpg"] = 1
            return app(environ, start_response)
        return filter_jpg
    
    def png_filter(self, app):
        def filter_png(environ, start_response):
            environ["khan.test.png"] = 1
            return app(environ, start_response)
        return filter_png
    
    def test(self):
        app = FilterDispatcher(self.print_pathinfo)
        rules = {
             "/(.*)\.jpg" : self.jpg_filter,
             "/(.*)\.png" : self.png_filter
             }
        for rule, filter_factory in rules.items():
            app[rule] = filter_factory
        self.test_app = TestApp(app)
        self.app = app
        resp = self.test_app.get("/ssaa/d/j/a//hsdasjdkja.jpg")
        self.assertTrue("khan.test.jpg" in resp.request.environ)
        resp = self.test_app.get("/ssaa/d/j/a//hsdasjdkja.png")
        self.assertTrue("khan.test.png" in resp.request.environ)
        resp = self.test_app.get("/x")
        self.assertTrue(resp.body == "/x")
        
class TestRuleDispatcher(TestCase):

    def test(self):
        dispatcher = RuleDispatcher(Response("app_default"))
        dispatcher[r"/(.*)\.jpg"] = Response("app_jpg")
        dispatcher[r"/(.*)\.png"] = Response("app_png")
        dispatcher = TestApp(dispatcher)
        resp = dispatcher.get("/ssaa/d/j/a//hsdasjdkja.jpg")
        self.assertTrue("app_jpg" in resp.body)
        resp = dispatcher.get("/ssaa/d/j/a//hsdasjdkja.png")
        self.assertTrue("app_png" in resp.body)
        resp = dispatcher.get("/not matched")
        self.assertTrue("app_default" in resp.body)

class TestURLDecryptor(TestCase):
    
    secret = "123456"
    
    test_urls = [
                     "/abc",
                     "/sadada.jpg",
                     "asddsdsada",
                     "sadksjdjakj-/~..................." + "".join(map(lambda x : str(x), range(10000))),
                     "",
                     "/"]
    
    def print_pathinfo(self, environ, start_response):
        return Response(environ.get("PATH_INFO", ""))(environ, start_response)

    def setUp(self):
        app = URLDecryptor(self.print_pathinfo, self.secret)
        self.test_app = TestApp(app)
        self.app = app
    
    def test_encode(self):
        for url in self.test_urls:   
            eurl = urlencrypt(url, self.secret)
            assert urldecrypt(eurl, self.secret) == url, "error: %s" % url
            
    def test_middleware_decode(self):
        for url in self.test_urls:
            if not url.startswith("/"):
                url = "/" + url
            eurl = urlencrypt(url, self.secret)
            resp = self.test_app.get(eurl, status = "*")
            assert resp.status_int == 200, "error status: %s" % resp.status_int
            assert resp.body == url, "error body: %s" % resp.body
    
    def test_error_handler(self):
        resp = self.test_app.get("/abcs", status = "*")
        assert resp.status_int == 400, "error status: %s" % resp.status_int
     
    def test_not_found(self):
        eurl = urlencrypt("/abcs", self.secret)
        def not_found_app(environ, start_response):
            from paste import httpexceptions 
            extra = ""
            extra += '\nSCRIPT_NAME: %r' % environ.get('SCRIPT_NAME')
            extra += '\nPATH_INFO: %r' % environ.get('PATH_INFO')
            extra += '\nHTTP_HOST: %r' % environ.get('HTTP_HOST')
            app = httpexceptions.HTTPNotFound(
                environ['PATH_INFO'],
                comment=extra).wsgi_application
            return app(environ, start_response)
        app = URLDecryptor(not_found_app, self.secret)
        test_app = TestApp(app)
        resp = test_app.get(eurl, status = "*")
        self.assertTrue(resp.status_int == 404, "error status: %s" % resp.status_int)
        self.assertTrue(eurl in resp.body, "error: encoded '%s' url not in response(%s)" % (eurl, resp.body))
