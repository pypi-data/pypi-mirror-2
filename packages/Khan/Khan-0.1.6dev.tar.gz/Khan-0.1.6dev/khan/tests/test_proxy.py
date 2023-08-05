# -*- coding: utf-8 -*-

from khan.utils.testing import *
from khan.proxy import *

"""
TODO:

1. 测试 HTTPS
"""

class TestProxy(TestCase):
    
    TARGET = "http://www.google.com"
    
    def test(self):
        app = Proxy(self.TARGET)
        app = TestApp(app)
        resp = app.get("/", status = "*")
        self.assertEqual(resp.status_int, 200)
        self.assertEqual("google" in resp.body, True, resp.body)
        
    def test_timeout(self):
        # 0.1 秒就超时
        app = Proxy(self.TARGET, timeout = 0.01)
        app = TestApp(app)
        resp = app.get("/", status = "*")
        # 超时应该返回 502
        self.assertEqual(resp.status_int, 502)
    
    def test_server_not_found(self):
        # 构造一个不存在的主机
        app = Proxy("http://...")
        app = TestApp(app)
        resp = app.get("/", status = "*")
        # 找不到服务器应该返回 404
        self.assertEqual(resp.status_int, 404)

class TestTransparentProxy(TestCase):
    
    HOST = "www.google.com"
    
    def test(self):
        app = TransparentProxy(force_host = self.HOST)
        app = TestApp(app)
        resp = app.get("/", status = "*")
        self.assertEqual(resp.status_int, 200)
        self.assertEqual("google" in resp.body, True)
        
    def test_timeout(self):
        # 0.1 秒就超时
        app = TransparentProxy(force_host = self.HOST, timeout = 0.01)
        app = TestApp(app)
        resp = app.get("/", status = "*")
        # 超时应该返回 502
        self.assertEqual(resp.status_int, 502)
    
    def test_server_not_found(self):
        # 构造一个不存在的主机
        app = TransparentProxy(force_host = "...")
        app = TestApp(app)
        resp = app.get("/", status = "*")
        # 找不到服务器应该返回 404
        self.assertEqual(resp.status_int, 404)
              
if __name__ == "__main__":
    unittest.main()
