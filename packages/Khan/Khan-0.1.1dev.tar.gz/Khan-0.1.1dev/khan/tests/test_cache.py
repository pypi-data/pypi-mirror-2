#-*- coding: utf-8 -*-

import time, unittest
from khan.utils.testing import *
from khan.cache import * 

class TestEtagCached(TestCase):
    
    def app(self, environ, start_response):
        start_response("200 OK", [("content-type", "text/plain")])
        return [environ["PATH_INFO"]]
    
    def test_with_expires(self):
        app = etag_cached(2)(self.app)
        test_app = TestApp(app)
        resp = test_app.get("/a", status = "*")
        headers = [("If-None-Match", resp.headers["ETag"]), 
                   ("If-Modified-Since", resp.headers["Last-Modified"])]
        resp1 = test_app.get("/b", status = "*", headers = headers)
        self.failUnlessEqual(resp1.status_int, 304)
        
        # 测试虽然指定了 expires 但是已经超时的情况
        app = etag_cached(1)(self.app)
        test_app = TestApp(app)
        resp = test_app.get("/a", status = "*")
        headers = [("If-None-Match", resp.headers["ETag"]), 
                   ("If-Modified-Since", resp.headers["Last-Modified"])]
        time.sleep(1)
        resp1 = test_app.get("/b", status = "*", headers = headers)
        self.failUnlessEqual(resp1.status_int, 200)
        self.assertTrue("Etag" in resp1.headers)
        self.assertTrue("Last-Modified" in resp1.headers)
        self.assertTrue(resp.headers["ETag"] == resp1.headers["Etag"])
        self.failUnlessEqual(resp1.body, "/b")
    
    def test_no_expires(self):
        app = etag_cached()(self.app)
        test_app = TestApp(app)
        resp = test_app.get("/a", status = "*")
        headers = [("If-None-Match", resp.headers["ETag"]), 
                   ("If-Modified-Since", resp.headers["Last-Modified"])]
        resp1 = test_app.get("/b", status = "*", headers = headers)
        self.failUnlessEqual(resp1.status_int, 304)
        
class TestCached(TestCase):
    
    def app(self, environ, start_response):
        # 每次都返回不一样结果的 app
        start_response("200 OK", [("content-type", "plain/text")])
        body = str(time.time())
        return [body]
        
    def test_no_cache(self):
        # 返回404 的 app
        def app(environ, start_response):
            start_response("404 Not Found", [("content-type", "plain/text")])
            body = str(time.time())
            return [body]
        app = cached(catch_status = [200])(app)
        test_app = TestApp(app)
        resp1 = test_app.get("/", status = "*")
        time.sleep(1)
        resp2 = test_app.get("/", status = "*")
        # app 返回客户端错误状态时， Cache 中间件应该不改变 app 返回的任何内容，包括 headers 和 status
        assert resp1.status_int == 404 and resp2.status_int == 404
        # 因为 app 总是返回 404，所以不缓存，那么两次的请求结果应该是*** 不一样 *** 的
        assert resp1.body != resp2.body, "resp1 body is : %s" % resp1.body
        
    def test_no_expires(self):
        app = cached()(self.app)
        test_app = TestApp(app)
        resp1 = test_app.get("/")
        time.sleep(1)
        resp2 = test_app.get("/")
        # 因为有缓存的原因，两次的请求结果应该是一样的
        assert resp1.body == resp2.body
    
    def test_with_expires(self):
        cur_body = []
        # 每次都返回不一样结果的 app
        def app(environ, start_response):
            start_response("200 OK", [("content-type", "plain/text")])
            body = str(time.time())
            cur_body = []
            cur_body.append(body)
            return [body]
        expires = 2
        app = cached(expires = expires)(app)
        test_app = TestApp(app)
        resp1 = test_app.get("/")
        time.sleep(1)
        resp2 = test_app.get("/")
        # 因为有缓存的原因，两次的请求结果应该是一样的
        assert resp1.body == resp2.body
        # 睡眠直到缓存过期
        time.sleep(expires)
        resp3 = test_app.get("/")
        # 因为第三次请求时缓存已经过期，那么第三次的结果应该和第一次的不一样
        assert resp3.body != resp1.body

if __name__ == "__main__":
    unittest.main()
