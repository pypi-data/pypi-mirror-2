# -*- coding: utf-8 -*-

from webob import Response, Request
from khan import schema
from khan.controller import *
from khan.controller.inspect_caller import *
from khan.utils.decorator import HTTPStatusOnInvalid
from khan.utils.testing import *

class DefaultControllerCase(Controller):
    
    @Expose()
    def index(self):
        return Response("index")
    
    @Expose()
    def _isnotaction(self):
        return Response("isnotaction")
    
    def notexposedaction(self):
        return Response("notexposedaction")
    
    @Expose()
    def action1(self):
        return Response("action1")

class DefaultActionResolveCase(Controller):
    
    @Expose()
    def index(self):
        return Response("index")
    
    @Expose()
    def action1(self):
        return Response("action1")
    
class CustomActionResolveCase1(DefaultActionResolveCase):
    
    @Expose()
    def myaction(self):
        return Response("myaction")
    
    def __action__(self, req):
        return "myaction"

class CustomActionResolveCase2(DefaultActionResolveCase):
    
    def notexposedaction(self):
        return Response("notexposedaction")
    
    def __resolve__(self, req, action):
        return lambda controller : self.notexposedaction()
    
class CustomBeforeAndAfterCase(DefaultActionResolveCase):
    
    @Expose()
    def realaction(self):
        return Response("realaction")
    
    def __before__(self, req):
        req.path_info = "/realaction"
        return req
    
    def __after__(self, resp):
        resp.body = resp.body + "_after"
        return resp
    
class TestController(TestCase):
    
    def test_basic(self):
        c = DefaultControllerCase()
        req = Request.blank("/_isnotaction")
        resp = c(req)
        self.assertEqual(404, resp.status_int)
        req = Request.blank("/notexposedaction")
        resp = c(req)
        self.assertEqual(404, resp.status_int)
        
    def test_action_resolve(self):
        app = TestApp(DefaultActionResolveCase())
        resp = app.get("/")
        self.assertEqual(200, resp.status_int)
        self.assertEqual("index", resp.body)
        resp = app.get("/action1/abc")
        self.assertEqual("action1", resp.body)
        resp = app.get("/action1/abc/")
        self.assertEqual("action1", resp.body)
        resp = app.get("/action1/abc/c/d/d/e/?")
        self.assertEqual("action1", resp.body)
        
        app = TestApp(DefaultActionResolveCase(default = "noaction"))
        resp = app.get("/abc", status = "*")
        self.assertEqual(404, resp.status_int)
        
        app = TestApp(CustomActionResolveCase1())
        resp = app.get("/abc")
        self.assertEqual("myaction", resp.body)
        
        app = TestApp(CustomActionResolveCase2())
        resp = app.get("/abc")
        self.assertEqual("notexposedaction", resp.body)
    
    def test_before_after(self):
        app = TestApp(CustomBeforeAndAfterCase())
        resp = app.get("/")
        self.assertEqual(200, resp.status_int)
        self.assertEqual("realaction_after", resp.body)
    
class InspectCallerCase(Controller):
    
    @InspectCaller(schema.Schema(id = schema.String()))
    def from_params(self, id):
        return Response(id)
    
    @InspectCaller(schema.Schema(id = schema.String()), POST)
    def from_post(self, id):
        return Response(id)

    @InspectCaller(schema.Schema(id = schema.String()), GET)
    def from_get(self, id):
        return Response(id)
    
    @InspectCaller(schema.Schema(id = schema.String()), URLParam("/from_url/{id}"))
    def from_url(self, id):
        return Response(id)
    
    @InspectCaller(schema.Schema(id = schema.String(), id1 = schema.String()), GET & POST & URLParam("/from_and/{id}"))
    def from_and(self, id, id1):
        return Response(id + id1)
    
    @InspectCaller(schema.Schema(id = schema.Int()), HTTPStatusOnInvalid(404))
    def invalid(self, id):
        return Response(id)
    
class TestInspectCaller(TestCase):
    
    def setUp(self):
        self.app = TestApp(InspectCallerCase())

    def test_basic(self):
        id = "1"
        id1 = "2"
        self.assertEqual(id, self.app.get('/from_params', {"id" : id}).body)
        self.assertEqual(id, self.app.post('/from_params', {"id" : id}).body)
        self.assertEqual(id, self.app.post('/from_post', {"id" : id}).body)
        self.assertEqual(id, self.app.get('/from_get', {"id" : id}).body)
        self.assertEqual(id, self.app.get('/from_url/%s' % id).body)
        self.assertEqual(id + id1, self.app.get('/from_and/%s' % id, {"id1" : id1}).body)
    
    def test_on_invalid(self):
        self.assertEqual(404, self.app.get('/invalid', {"id" : "not_int"}, status = "*").status_int)
        
if __name__ == "__main__":
    unittest.main()
    