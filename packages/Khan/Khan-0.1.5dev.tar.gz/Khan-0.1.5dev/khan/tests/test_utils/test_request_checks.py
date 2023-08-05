# -*- coding: utf-8 -*-

from khan.utils.testing import *
from khan.utils import *
from khan.utils.request_checks import *
from khan.utils.decorator import HTTPStatusOnInvalid
from khan.httpstatus import HTTPStatus

class TestRequestChecks(TestCase):
    
    def test_request_check(self):
    
        def App(environ, start_response):
            return HTTPStatus(200)(environ, start_response)
        
        # test `on_invalid`
        app = TestApp(reqchecker(Equal(request_method = 'get', case_sensitive = True), HTTPStatusOnInvalid(404))(App))
        self.failUnlessEqual(app.get("/", status = "*").status_int, 404)
        
        # test `Egual`
        app = TestApp(reqchecker(Equal(request_method = 'GET'))(App))
        self.failUnlessEqual(app.get("/", status = "*").status_int, 200)
        
        # test `Egual` not case sensitive
        app = TestApp(reqchecker(Equal(request_method = 'get'))(App))
        self.failUnlessEqual(app.get("/", status = "*").status_int, 200)
        
        # test `Egual` case sensitive
        app = TestApp(reqchecker(Equal(request_method = 'get', case_sensitive = True))(App))
        self.failUnlessEqual(app.get("/", status = "*").status_int, 400)
        
        # test `Egual` key not exists
        app = TestApp(reqchecker(Equal(not_exists = 'not exists'))(App))
        self.failUnlessEqual(app.get("/", status = "*").status_int, 400)
        
        # test `or`
        app = TestApp(reqchecker(Equal(request_method = 'GET') | Equal(request_method = 'POST') | \
                               Equal(request_method = 'PUT'))(App))
        self.failUnlessEqual(app.get("/", status = "*").status_int, 200)
        self.failUnlessEqual(app.post("/", status = "*").status_int, 200)
        self.failUnlessEqual(app.put("/", status = "*").status_int, 200)
        
        # test `and`
        app = TestApp(reqchecker(Equal(request_method = 'GET') & Equal(path_info = '/'))(App))
        self.failUnlessEqual(app.get("/", status = "*").status_int, 200)
        self.failUnlessEqual(app.get("/path_info", status = "*").status_int, 400)
        self.failUnlessEqual(app.post("/", status = "*").status_int, 400)
        
        # test `not`
        app = TestApp(reqchecker(~Equal(request_method = 'GET'))(App))
        self.failUnlessEqual(app.get("/", status = "*").status_int, 400)
        self.failUnlessEqual(app.post("/", status = "*").status_int, 200)
        
if __name__ == "__main__":
    unittest.main()
    