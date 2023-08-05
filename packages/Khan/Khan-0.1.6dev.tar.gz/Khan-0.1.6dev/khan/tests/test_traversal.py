# -*- coding: utf-8 -*-

from khan.httpstatus import HTTPStatus
from khan.utils.testing import *
from khan.traversal import *

class TraverserTester(TestCase):
    
    def test_basic(self):
        traverser = Traverser()
        testapp = TestApp(traverser)
        resp = testapp.get("/a/b/c", status = "*")
        self.assertTrue(resp.status_int == 404)
        
    def test_default_app(self):
        traverser = Traverser(default = HTTPStatus(503))
        testapp = TestApp(traverser)
        resp = testapp.get("/a/b/c", status = "*")
        self.assertTrue(resp.status_int == 503)
    
    def test_with_graph(self):
        d = {
             "" : 1,
             "a2" : {"b" : 1},
             "a3" : {"b" : {"c" : 1}},
        }
        graph = DictModel(d)
        traverser = Traverser(graph)
        traverser["a"] = HTTPStatus(401)
        traverser["b"] = HTTPStatus(402)
        traverser["c"] = HTTPStatus(403)
        testapp = TestApp(traverser)
        resp_a = testapp.get("/a", status = "*")
        self.assertTrue(resp_a.status_int == 401)
        resp_b = testapp.get("/a2/b/b", status = "*")
        self.assertTrue(resp_b.status_int == 402)
        resp_c = testapp.get("/a3/b/c/c/e/f/g.h.txt", status = "*")
        self.assertTrue(resp_c.status_int == 403)
    
    def test_path_info(self):
        d = {
             "" : 1,
        }
        graph = DictModel(d)
        traverser = Traverser(graph)
        def app_path_info(environ, start_response):
            start_response("200 OK", [("content-type", "text/plain")])
            return [environ["PATH_INFO"]]
        def app_script_name(environ, start_response):
            start_response("200 OK", [("content-type", "text/plain")])
            return [environ["SCRIPT_NAME"]]
        traverser["a3"] = app_path_info
        traverser["a4"] = app_script_name
        testapp = TestApp(traverser)
        resp = testapp.get("/a3/b/c/c/e/f/g.h.txt")
        self.assertTrue(resp.body == "/b/c/c/e/f/g.h.txt")
        resp1 = testapp.get("/a4/b/c/c/e/f/g.h.txt")
        self.failUnlessEqual(resp1.body, "/a4")
        
if __name__ == "__main__":
    unittest.main()
