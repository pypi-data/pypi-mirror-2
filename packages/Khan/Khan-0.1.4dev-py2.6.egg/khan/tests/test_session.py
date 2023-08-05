# -*- coding: utf-8 -*-

import time, os
from tempfile import mktemp
from Cookie import SimpleCookie
from khan.utils.testing import *
from khan.store import *
from khan.session import *

class SessionContainerTester(DictTester, TestCase):
    
    def setUp(self):
        self.store = SessionContainer.create(dict())
        super(SessionContainerTester, self).setUp()
        
class TestSessionMiddleware(TestCase):

    def __init__(self, *args, **kargs):
        TestCase.__init__(self, *args, **kargs)
        self.db_files = []
        
    def tearDown(self):
        for db_file in self.db_files:
            if os.path.isfile(db_file):
                os.remove(db_file)
        
    def make_session_app(self, app, store = None, identifiers = None, expires = None):
        db_file = mktemp()
        self.db_files.append(db_file)
        if store is None:
            store = get_backend("khan.dbm://%s" % db_file)
        session_store = store
        assert_dict(session_store)
        app = SessionMiddleware(app, session_store, identifiers = identifiers, expires = expires)
        return TestApp(app)

    def test_nosession(self):
        test_app = self.make_session_app(PrintValue("value"))
        resp = test_app.get("/")
        assert "Set-Cookie" not in resp.headers
        assert resp.body == "value"
    
    def test_cookie(self):
        def app(environ, start_response):
            if "a" not in session:
                session["a"] = "1"
                session.save()
            start_response("200 OK", [("content-type", "text/plain")])
            return [session["a"]]
        test_app = self.make_session_app(app)
        resp = test_app.get("/")
        assert "Set-Cookie" in resp.headers
        assert resp.body == "1"
        
    def test_expires(self):
        def app(environ, start_response):
            if "a" not in session:
                session["a"] = "1"
                session.save()
            start_response("200 OK", [("content-type", "text/plain")])
            return [session["a"]]
        expires = 3
        test_app = self.make_session_app(app, expires = expires)
        
        resp = test_app.get("/")
        assert "Set-Cookie" in resp.headers
        cookie = SimpleCookie(resp.headers["Set-Cookie"])
        
        # 此时 session 已经建立，服务器不应该再返回 set-cookie 的头
        resp = test_app.get("/", [("Cookie", "%s=%s" \
                                               % (CookieIdentifier.COOKIE_NAME, cookie[CookieIdentifier.COOKIE_NAME].value))])
        assert "Set-Cookie" not in resp.headers
        
        # 睡眠直到 session 过期
        time.sleep(expires + 1)
        
        # 此时 session 已经过期，服务器应该再返回 set-cookie 的头
        resp = test_app.get("/", [("Cookie", "%s=%s" \
                                               % (CookieIdentifier.COOKIE_NAME, cookie[CookieIdentifier.COOKIE_NAME].value))])
        assert "Set-Cookie" in resp.headers
        
        cookie = SimpleCookie(resp.headers["Set-Cookie"])
        # 不断地发送请求，使 session 的到期时间不断更新
        for i in range(expires + 1):
            time.sleep(1)
            resp = test_app.get("/", [("Cookie", "%s=%s" \
                                               % (CookieIdentifier.COOKIE_NAME, cookie[CookieIdentifier.COOKIE_NAME].value))])
            # 此时 session 不应该已过期
            assert "Set-Cookie" not in resp.headers
        
        # 睡眠直到 session 过期
        time.sleep(expires + 1)
        
        # 此时 session 已经过期，服务器应该再返回 set-cookie 的头
        resp = test_app.get("/", [("Cookie", "%s=%s" \
                                               % (CookieIdentifier.COOKIE_NAME, cookie[CookieIdentifier.COOKIE_NAME].value))])
        assert "Set-Cookie" in resp.headers
    
    def test_httpheaderidentifier(self):
        def app(environ, start_response):
            if "a" not in session:
                session["a"] = "1"
                session.save()
            start_response("200 OK", [("content-type", "text/plain")])
            return [session["a"]]
        expires = 3
        test_app = self.make_session_app(app, identifiers = HTTPHeaderIdentifier(), expires = expires)
        resp = test_app.get("/")
        assert HTTPHeaderIdentifier.HEADER_NAME in resp.headers
        sid = resp.headers[HTTPHeaderIdentifier.HEADER_NAME]
        # 此时 session 已经建立，服务器不应该再返回 set-cookie 的头
        resp = test_app.get("/a", [], {HTTPHeaderIdentifier.HEADER_NAME : sid})
        assert HTTPHeaderIdentifier.HEADER_NAME not in resp.headers

if __name__ == "__main__":
    unittest.main()
