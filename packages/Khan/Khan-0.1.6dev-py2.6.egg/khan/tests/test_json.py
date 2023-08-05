# -*- coding: utf-8 -*-

from khan.utils.testing import *
from khan.utils import unique_id
from khan.json import *

class TestJSONRPCError(TestCase):
    
    def test(self):
        for ecode, cls in jsonrpc_error_map.items():
            def wsgi_app(environ, start_response):
                resp = cls()
                return resp(environ, start_response)
            test_app = TestApp(wsgi_app)
            resp = test_app.get("/", status = "*")
            self.failUnlessEqual(resp.status_int, 200)
            json_data = jsonrpc_loads(resp.body)
            self.failUnlessEqual(json_data["error"]["message"], cls.message)
            self.failUnlessEqual(json_data["error"]["code"], cls.code)
            
class TestJSONPProxy(TestCase):
    
    def setUp(self):
        self.app = JSONPProxy()
        self.test_app = TestApp(self.app)
        
    def test(self):
        param = {"_callback" : "abc"}
        extra_environ = {"HTTP_HOST" : "w3c.org"}
        resp = self.test_app.get("/400", status = "*", extra_environ = extra_environ)
        assert resp.status_int == 400, "error status: %d" % resp.status_int
        resp = self.test_app.get("/404", param, status = "*", extra_environ = extra_environ)
        self.assertEqual(502, resp.status_int)
        resp = self.test_app.get("/%s" % unique_id(), param, status = "*", extra_environ = extra_environ)
        self.assertEqual(502, resp.status_int)
        resp = self.test_app.get("/", param, status = "*", extra_environ = extra_environ)
        self.assertEqual(200, resp.status_int)
        self.assertEqual("text/javascript", resp.content_type)
        
class TestJSONRPCService(TestCase):
    
    def setUp(self):
        self.app = JSONRPCService()
        self.app["test.echo"] = self.echo
        self.test_app = TestApp(self.app)
    
    def echo(self, s):
        return s

    def get_exc_from_resp(self, resp):
        json_resp = jsonrpc_loads(resp.body)
        exc = jsonrpc_error_map[json_resp["error"]["code"]]
        return exc
        
    def test_basic(self):
        # 测试按顺序的参数调用
        json_req = JSONRPCBuilder.request("test.echo", "a", id = 10)
        resp = self.test_app.post("/", json_req, status = "*")
        assert resp.status_int == 200
        json_resp = jsonrpc_loads(resp.body)
        self.assertEqual(json_resp['id'], 10)
        assert json_resp["result"] == "a", "req: %s,  resp: %s" % (json_req,  json_resp)
        
        # 测试按名字的参数调用
        json_req = JSONRPCBuilder.request("test.echo", {"s" : "a"}, id = 0)
        resp = self.test_app.post("/", json_req, status = "*")
        json_resp = jsonrpc_loads(resp.body)
        assert json_resp["result"] == "a", "req: %s,  resp: %s" %(json_req,  json_resp)
        
        # URL 应该全部被 handle ， 仍然会返回 200
        resp = self.test_app.post("/not_implemented", json_req, status = "*")
        assert resp.status_int == 200
        
        # 测试 jsonrpc 版本
        for version in [None, '1.0', '2.0']:
            json_req = JSONRPCBuilder.request("test.echo", [1], version = version, id = 2)
            resp = self.test_app.post("/", json_req, status = "*")
            json = jsonrpc_loads(resp.body)
            self.assertEqual(json['result'], 1)
            self.assertEqual(json['id'], 2)
            self.assertFalse(json.has_key('error'))
            if version == '1.0':
                self.assertTrue(json.has_key('version'))
                self.assertEqual(json['version'], '1.0')
            elif version == '2.0':
                self.assertTrue(json.has_key('jsonrpc'))
                self.assertEqual(json['jsonrpc'], '2.0')
            else:
                self.assertTrue(json.has_key('version'))
                self.assertEqual(json['version'], '1.0')
            
    def test_with_invalid_request(self):
        # get 方式
        resp = self.test_app.get("/", status = "*")
        # 仍然会返回 200
        assert resp.status_int == 200
        exc = self.get_exc_from_resp(resp)
        # 应该返回 JSONRPCInvalidRequestError
        assert JSONRPCInvalidRequestError == exc
        # 发送无效的 jsonrpc 请求数据
        resp = self.test_app.post("/", "invalid jsonrpc data", status = "*")
        exc = self.get_exc_from_resp(resp)
        # 应该返回 JSONRPCParseError
        assert JSONRPCParseError == exc
        json_req = JSONRPCBuilder.request("", "a")
        # 发送无效的方法名
        resp = self.test_app.post("/", json_req, status = "*")
        exc = self.get_exc_from_resp(resp)
        # 应该返回 JSONRPCParseError
        assert JSONRPCParseError == exc
        
    def test_method_not_found(self):
        json_req = JSONRPCBuilder.request("no method", "a", id = 0)
        resp = self.test_app.post("/", json_req, status = "*")
        exc = self.get_exc_from_resp(resp)
        # 应该返回 JSONRPCMethodNotFoundError
        assert JSONRPCMethodNotFoundError == exc
        
    def test_invalid_params(self):
        json_req = JSONRPCBuilder.request("test.echo", id = 0)
        resp = self.test_app.post("/", json_req, status = "*")
        exc = self.get_exc_from_resp(resp)
        # 应该返回 JSONRPCInvalidParamsError
        assert JSONRPCInvalidParamsError == exc
        
    def test_internal_error(self):
        def raise_error():
            raise ValueError("raised")
        self.app["test.raise_error"] = raise_error
        json_req = JSONRPCBuilder.request("test.raise_error", id = 0)
        resp = self.test_app.post("/", json_req, status = "*")
        exc = self.get_exc_from_resp(resp)
        # 应该返回 JSONRPCInvalidRequestError
        assert JSONRPCInternalError == exc
        
    def test_notification_req(self):
        json_req = JSONRPCBuilder.request("test.echo", [1])
        resp = self.test_app.post("/", json_req, status = "*")
        self.assertFalse(resp.body)
        # 无效参数下也不返回数据
        json_req = JSONRPCBuilder.request("test.echo")
        resp = self.test_app.post("/", json_req, status = "*")
        self.assertFalse(resp.body)
        # 找不到方法下也不返回数据
        json_req = JSONRPCBuilder.request("test.nomethod", [1])
        resp = self.test_app.post("/", json_req, status = "*")
        self.assertFalse(resp.body)

if __name__ == "__main__":
    unittest.main()
    