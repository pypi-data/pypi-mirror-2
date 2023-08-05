# -*- coding: utf-8 -*-

from khan.utils.testing import *
from khan.virtualhost import *

class TestVirtualHost(TestCase):
    
    def setUp(self):
        vhost = VirtualHost()
        vhost["domain.com"] = PrintValue("domain.com:80")
        vhost["*:*"] = PrintValue("*:*")
        vhost["*:80"] =  PrintValue("*:80")
        vhost["www.domain.com:*"] = PrintValue("www.domain.com:*")
        vhost["a.www.domain.com:*"] = PrintValue("a.www.domain.com:*")
        vhost["*.domain.com:80"] = PrintValue("*.domain.com:80")
        vhost["ex.com:80"] = PrintValue("ex.com:80")
        vhost["*.*.domain.com:990"] = PrintValue("*.*.domain.com")
        vhost["*.ex.com"] = PrintValue("*.ex.com")
        vhost["*.*.ex.com:80"] = PrintValue("*.*.ex.com:80")
        vhost["*.*.*.a.com"] = PrintValue("*.*.*.a.com")
        self.app = TestApp(vhost)
        self.vhost = vhost
        
    def test_match(self):
        resp = self.app.get("/", extra_environ = {"HTTP_HOST" : "a.www.domain.com", "HTTP_PORT" : "80"})
        assert resp.body == "a.www.domain.com:*", resp.body 
    
    def test_not_found(self):
        resp = self.app.get("/", extra_environ = {"HTTP_HOST" : "a1.www.domain.com", "HTTP_PORT" : "80"})
        assert resp.status_int == 200
        del self.vhost["*:*"]
        resp = self.app.get("/", status = "*", extra_environ = {"HTTP_HOST" : "a1.www.domain.com", "HTTP_PORT" : "880"})
        assert resp.status_int == 404, resp.body
        self.vhost["*:*"] = PrintValue("*:*")
        