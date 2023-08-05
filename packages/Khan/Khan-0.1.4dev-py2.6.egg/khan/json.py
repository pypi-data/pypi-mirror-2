# -*- coding: utf-8 -*-

"""
json 工具
=================================

本模块提供 json 和 jsonrpc 工具.

索引
=================================

* :data:`JSON_MIME_TYPE`
* :attr:`request`
* :attr:`jsonrpc_error_map`
* :func:`jsonrpc_loads`
* :func:`dump_to_json_response`
* :class:`JSONRPCBuilder`
* :class:`JSONRPCError`
* :class:`JSONRPCParseError`
* :class:`JSONRPCInvalidRequestError`
* :class:`JSONRPCMethodNotFoundError`
* :class:`JSONRPCInvalidParamsError`
* :class:`JSONRPCInternalError`
* :class:`JSONRPCServerError`
* :class:`JSONRPCService`
* :class:`JSONRPCClient`
* :class:`JSONPProxy`
* :class:`JSONPMiddleware`
* :func:`make_jsonpproxy_app`
* :func:`make_jsonrpc_app`
* :func:`make_jsonp_middleware`
* :func:`make_jsonrpc_client_object`
* :class:`JSONRPCClientCommand`

=================================

.. autodata:: JSON_MIME_TYPE

.. attribute:: request

    为 JSONRPCService 注册此变量提供方便的 request 访问

.. attribute:: jsonrpc_error_map
.. autofunction:: jsonrpc_loads
.. autofunction:: dump_to_json_response
.. autoclass:: JSONRPCBuilder
    :members:
.. autoclass:: JSONRPCError
.. autoclass:: JSONRPCParseError
.. autoclass:: JSONRPCInvalidRequestError
.. autoclass:: JSONRPCMethodNotFoundError
.. autoclass:: JSONRPCInvalidParamsError
.. autoclass:: JSONRPCInternalError
.. autoclass:: JSONRPCServerError
.. autoclass:: JSONRPCService
.. autoclass:: JSONRPCClient
    :members:
.. autoclass:: JSONPProxy
.. autoclass:: JSONPMiddleware
.. autofunction:: make_jsonpproxy_app
.. autofunction:: make_jsonrpc_app
.. autofunction:: make_jsonp_middleware
.. autofunction:: make_jsonrpc_client_object
.. autoclass:: JSONRPCClientCommand
"""

import logging, types, os, traceback, platform
from UserDict import DictMixin
import httplib2
import simplejson
from paste.request import construct_url
from paste.registry import StackedObjectProxy, RegistryManager
from paste.util.import_string import eval_import
from simplejson import dumps, loads
from webob import Request, Response
from webob.exc import HTTPException, status_map
from khan.httpstatus import HTTPStatus
from khan.proxy import TransparentProxy
from khan.command import Command

__all__ = [
   "JSON_MIME_TYPE",
   "dumps",
   "loads",
   "dump_to_json_response",
   "request",
   "JSONPProxy",
   "JSONPMiddleware",
   "jsonrpc_loads",
   "jsonrpc_error_map",
   "JSONRPCBuilder",
   "JSONRPCService",
   "JSONRPCClient",
   "JSONRPCError",
   "JSONRPCParseError",
   "JSONRPCInvalidRequestError",
   "JSONRPCMethodNotFoundError",
   "JSONRPCInvalidParamsError",
   "JSONRPCInternalError",
   "JSONRPCServerError"
]

#: JSON 的 mimetype
JSON_MIME_TYPE = "application/json"

# 为 JSONRPCService 提供方便的 request 访问
request = StackedObjectProxy(name = "request")

#: 错误码与 :class:`JSONRPCError` 子类映射关系
jsonrpc_error_map = {}

if platform.system().lower() in ["linux", "unix"]:
    EX_SOFTWARE = os.EX_SOFTWARE
    EX_OK = os.EX_OK
else:
    # 重新按照 Linux 下 的常量定义
    EX_SOFTWARE = 70
    EX_OK = 0
    
def dump_to_json_response(json_data, encoding = "utf-8", **keyword):
    """
    转换 Python 对象到 webob.Response 对象

    :param json_data: python object
    :param encoding: encoding

    :rtype: `webob.Response`
    """

    body = dumps(json_data)
    resp = Response(body, content_type = JSON_MIME_TYPE, **keyword)
    resp.content_encoding = encoding
    return resp

class JSONRPCBuilder(object):
    """
    构建 jsonrpc 格式字符串

    .. seealso::

        参见 jsonrpc 协议
    """

    @staticmethod
    def request(method, params = None, id = 0, version = "2.0"):
        """
        构建 jsonrpc 请求

        :param method: method name
        :param params: params, list or dict
        :param id: id
        :param version: jsonrpc protocol version, defualts is 2.0

        :type method: string
        :type id: int
        :type version: string

        :rtype: string
        """

        fversion = float(version)
        if fversion >= 2.0:
            version_field_name = 'jsonrpc'
        else:
            version_field_name = 'version'    
        id = int(id)
        if params:
            params_type = type(params)
            if params_type is tuple:
                params = list(params)
            elif params_type not in [dict, list]:
                params = [params]
            json_str = "{\"%(version_field_name)s\":\"%(version)s\", \"method\":\"%(method)s\", \"params\":%(params)s, \"id\":%(id)s}" \
                        % dict(version_field_name = version_field_name, version = version, method = method, params = dumps(params), id = id)
        else:
            json_str = "{\"%(version_field_name)s\":\"%(version)s\", \"method\":\"%(method)s\", \"id\":%(id)s}" \
                        % dict(version_field_name = version_field_name, version = version, method = method, id = id)
        return json_str

    @staticmethod
    def response(result = None, error = None, id = 0, version = "2.0"):
        """
        构建 jsonrpc 响应

        :param result: python object
        :param error: :class:`JSONRPCError`
        :param id: id
        :param version: jsonrpc protocol version, defualts is 2.0

        :rtype: string
        """
        
        fversion = float(version)
        if fversion >= 2.0:
            version_field_name = 'jsonrpc'
        else:
            version_field_name = 'version'
        if error:
            if hasattr(error, 'data'):
                json_str = '''
                {"%(version_field_name)s":"%(version)s", "result":null, "error":{"code":%(code)s,"message":"%(message)s", "data" : "%(data)s"}, "id":null}
                ''' % dict(version_field_name = version_field_name, version = version, code = error.code, message = error.message or 'null', data = error.data or 'null')
            else:
                json_str = '''
                {"%(version_field_name)s":"%(version)s", "result":null, "error":{"code":%(code)d,"message":"%(message)s"}, "id":null}
                ''' % dict(version_field_name = version_field_name, version = version, code = int(error.code), message = error.message or 'null')
        else:
            id = int(id)
            json_str = '''
            {"jsonrpc":"%(version)s", "result":%(result)s, "error":null, "id":%(id)s}
            ''' % dict(version = version, result = dumps(result), id = id)
        return json_str

class JSONRPCErrorMeta(type):

    def __init__(cls, name, bases, attrs):
        jsonrpc_error_map[cls.code] = cls

class JSONRPCError(Exception, Response):
    """
    代表 jsonrpc 错误基类
    """

    __metaclass__ = JSONRPCErrorMeta

    message = "jsonrpc error."
    code = 0
    data = None

    def __init__(self, message = None, code = None, data = None):
        """
        :param code:
            A Number that indicates the actual error that occurred. This MUST be an integer.

        :param message:
            A String providing a short description of the error. The message SHOULD be limited to a concise single sentence.

        :param data:
            Additional information, may be omitted. Its contents is entirely defined by the application (e.g. detailed error information, nested errors etc.).
        """

        if message:
            self.message = message
        if code:
            self.code = int(code)
        if data:
            self.data = data
        Exception.__init__(self, self.message)
        Response.__init__(self, status = "200 OK")

    def __call__(self, environ, start_response):
        self.body = JSONRPCBuilder.response(error = self)
        self.content_type = JSON_MIME_TYPE
        self.content_encoding = "utf-8"
        return super(JSONRPCError, self).__call__(environ, start_response)

class JSONRPCParseError(JSONRPCError):
    """ jsonrpc 协议分析错误 """

    code = -32700
    message = "Parse error."

class JSONRPCInvalidRequestError(JSONRPCError):
    """ jsonrpc 请求无效错误 """

    code = -32600
    message = "Invalid Request."

class JSONRPCMethodNotFoundError(JSONRPCError):
    """ jsonrpc 方法不存在错误 """

    code = -32601
    message = "Method not found."

class JSONRPCInvalidParamsError(JSONRPCError):
    """ jsonrpc 调用方法的参数无效错误 """

    code = -32602
    message = "Invalid params."

class JSONRPCInternalError(JSONRPCError):
    """ jsonrpc 内部错误 """

    code = -32603
    message = "Internal error."

class JSONRPCServerError(JSONRPCError):
    """ jsonrpc 服务器错误 """

    code = -32000
    message = "Server error."

def jsonrpc_loads(data, version = None):
    """
    将一个 jsonrpc 格式字符串转换为 python object 并返回

    :param data: jsonrpc 字符串
    :param version: protocol version

    :rtype: python object
    """

    jsonrpc_data = loads(data)
    assert "id" in jsonrpc_data, JSONRPCParseError("`id` field invalid")
    if version:
        fversion = float(version)
        if fversion >= 2.0:
            version_field_name = 'jsonrpc'
        else:
            version_field_name = 'version'
        assert version_field_name in jsonrpc_data, JSONRPCParseError("`%s` field missing." % version_field_name)
    else:
        assert ('version' in jsonrpc_data) or ('jsonrpc' in jsonrpc_data), JSONRPCParseError("`version` or `jsonrpc` field missing.")
    if "method" in jsonrpc_data and isinstance(jsonrpc_data["method"], basestring):
        jsonrpc_data["method"] = jsonrpc_data["method"].strip()
        assert jsonrpc_data["method"], JSONRPCParseError("`method` field invalid.")
        if "params" in jsonrpc_data:
            assert type(jsonrpc_data["params"]) in [list, dict], JSONRPCParseError("`params` field invalid.")
    else:
        assert "result" in jsonrpc_data, JSONRPCParseError("`result` field missing")
        assert "error" in jsonrpc_data, JSONRPCParseError("`error` field missing")
        if jsonrpc_data["result"]:
            assert jsonrpc_data["error"] == None, JSONRPCParseError("`error` field must be `null`")
        else:
            if jsonrpc_data["error"]:
                assert jsonrpc_data["id"] == None, JSONRPCParseError("`id` field must be null.")
                assert "code" in jsonrpc_data["error"] and (type(jsonrpc_data["error"]["code"]) is int) \
                    and "message" in jsonrpc_data["error"] \
                    and isinstance(jsonrpc_data["error"]["message"], basestring), JSONRPCParseError("`code` or `messgae` fields invalid.")
    return jsonrpc_data

class JSONRPCService(DictMixin, object):
    """
    提供 jsonrpc 服务的 WSGI app, 本类实现了 Dict 接口，并且注册 ``request`` 变量

    示例::

        app = JSONRPCService()
        app["test.echo"] = lambda data: data
    """

    def __init__(self, *args, **kargs):
        self._factory = dict(*args, **kargs)
        self._logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
        self._wapper_app = RegistryManager(self._wapper_call)

    def __setitem__(self, name, provider):
        assert callable(provider), ValueError("provider `%r` not callable" % self.get_provider_name(provider))
        self._factory[name] = provider

    def __delitem__(self, name):
        del self._factory[name]

    def __getitem__(self, name):
        return self._factory[name]

    def keys(self):
        return self._factory.keys()

    def get_provider_name(self, provider):
        if type(provider) is types.ClassType:
            return provider.__class__.__name__
        else:
            if hasattr(provider, "__name__"):
                return provider.__name__
            else:
                return "%s" % provider
    
    def method_resolve(self, method):
        if method not in self._factory:
            return None
        else:
            return self._factory[method]
            
    def _wapper_call(self, environ, start_response):
        req = Request(environ)
        reg = environ.get("paste.registry", None)
        if reg:
            reg.register(request, req)
        if not req.method == "POST":
            self._logger.debug("request method '%s' not accepted." % req.method)
            resp = Response(JSONRPCBuilder.response(error = JSONRPCInvalidRequestError()),
                            content_type = JSON_MIME_TYPE, charset = 'utf-8')
            return resp(environ, start_response)
        post_data = req.body.strip()
        try:
            jsonrpc_data = jsonrpc_loads(post_data)
        except:
            self._logger.debug("post data invalid: %r" % post_data, exc_info = True)
            resp = Response(JSONRPCBuilder.response(error = JSONRPCParseError()),
                            content_type = JSON_MIME_TYPE, charset = 'utf-8')
            return resp(environ, start_response)
        if 'version' in jsonrpc_data:
            version = jsonrpc_data['version']
        elif 'jsonrpc' in jsonrpc_data:
            version = jsonrpc_data['jsonrpc']
        else:
            self._logger.debug("the 'version' or 'jsonrpc' field missing." % post_data, exc_info = True)
            resp = Response(JSONRPCBuilder.response(error = JSONRPCParseError()),
                            content_type = JSON_MIME_TYPE, charset = 'utf-8')
            return resp(environ, start_response)
        if "method" not in jsonrpc_data:
            self._logger.debug("`method` field not found.")
            resp = Response(JSONRPCBuilder.response(error = JSONRPCParseError(), version = version),
                            content_type = JSON_MIME_TYPE, charset = 'utf-8')
            return resp(environ, start_response)
        args = []
        kargs = {}
        if "params" in jsonrpc_data:
            params_type = type(jsonrpc_data["params"])
            if params_type in [list, tuple]:
                args = jsonrpc_data["params"]
            else:
                kargs = jsonrpc_data["params"]
                new_kargs = {}
                # kargs 的所有 keys 值有可能为 unicode，必须转码
                for k, v in kargs.items():
                    if isinstance(k, unicode):
                        k = k.encode("utf-8")
                    new_kargs[k] = v
                kargs = new_kargs
        provider = self.method_resolve(jsonrpc_data["method"])
        if provider is None:
            self._logger.debug("method '%s' not found." % jsonrpc_data["method"])
            resp = Response(JSONRPCBuilder.response(error = JSONRPCMethodNotFoundError(), version = version),
                            content_type = JSON_MIME_TYPE, charset = 'utf-8')
            return resp(environ, start_response)
        
        environ["khan.web.service"] = self

        self._logger.debug("calling `%r` service with keyword args(*%r) and kargs(**%r)" 
                           % (self.get_provider_name(provider), args, kargs))
        try:
            result = provider(*args, **kargs)
            resp = Response(JSONRPCBuilder.response(result = result, id = jsonrpc_data["id"], version = version),
                            content_type = JSON_MIME_TYPE, charset = 'utf-8')
            return resp(environ, start_response)
        except HTTPException, httpe:
            self._logger.debug("`%r` raised HTTPException: %s (code: %s)",
                      provider, httpe.__class__.__name__,
                      httpe.wsgi_response.code, exc_info=True)
            # 304 Not Modified's shouldn't have a content-type set
            if httpe.wsgi_response.status_int == 304:
                httpe.wsgi_response.headers.pop('Content-Type', None)
            return httpe(environ, start_response)
        except TypeError, e:
            self._logger.error("calling `%r` with invalid arguments." % self.get_provider_name(provider), exc_info = True)
            resp = Response(JSONRPCBuilder.response(error = JSONRPCInvalidParamsError(), 
                                                    id = jsonrpc_data["id"], version = version),
                            content_type = JSON_MIME_TYPE, charset = 'utf-8')
            return resp(environ, start_response)
        except JSONRPCError, e:
            self._logger.error("jsonrpc error.", exc_info = True)
            resp = Response(JSONRPCBuilder.response(error = e, id = jsonrpc_data["id"], version = version),
                            content_type = JSON_MIME_TYPE, charset = 'utf-8')
            return resp(environ, start_response)
        except:
            self._logger.error("`%r` raised unknown exception." % self.get_provider_name(provider), exc_info = True)
            resp = Response(JSONRPCBuilder.response(error = JSONRPCInternalError(), 
                                                    id = jsonrpc_data["id"], version = version),
                            content_type = JSON_MIME_TYPE, charset = 'utf-8')
            return resp(environ, start_response)

    def __call__(self, environ, start_response):
        return self._wapper_app(environ, start_response)

def make_jsonrpc_app(global_conf, **providers):
    """
    paste EGG Entry Point::

        jsonrpc

    用 PasteDeploy 部署::

        [app:jsonrpc]
        use = egg:khan#jsonrpc
        echo = your_func
    """

    app = JSONRPCService()
    for uri, import_name in providers.items():
        provider = eval_import(import_name)
        app[uri] = provider
    return app

class JSONRPCClient(object):
    """
     jsonrpc 客户端

     使用示例::

         client = JSONRPCClient("https://localhost:8888/")
         result = client.test.echo("bbbb")
         result1 = client.test.echo(data = "bbbb")
         assert result == result1
    """

    default_headers = {
            "Content-type": JSON_MIME_TYPE,
            "Accept": "text/plain"
    }

    def __init__(self, url, timeout = None, service_name = None, http_headers = None, version = "2.0", http_client = None, id = 0):
        """
        :param url: jsonrpc 服务 url, 支持 https.
        :param timeout: socket 级的 timeout(秒) 设置.
        """

        self._http_client = http_client or httplib2.Http(timeout = timeout)
        self._timeout = timeout
        self._url = url
        self._service_name = service_name
        self._http_headers = http_headers or {}
        self._version = version
        self._id = id

    def add_credentials(self, username, password = None):
        """ 如果服务器要求身份验证，可使用本函数添加用户名和密码 """

        return self._http_client.add_credentials(username, password or "")

    def __getattr__(self, name):
        if (self._service_name != None):
            name = "%s.%s" % (self._service_name, name)
        return JSONRPCClient(self._url, self._timeout, name, self._http_headers, version = self._version, http_client = self._http_client, id = self._id)

    def __call__(self, *args, **kargs):
        """
        `*args` 和 `**kargs` 参数不能同时提供，参见 jsonrpc 2.0 标准
        """

        http_headers = {}
        http_headers.update(self.default_headers)
        http_headers.update(self._http_headers)
        if args:
            params = args
        elif kargs:
            params = kargs
        else:
            params = None
        self._id += 1
        post_data = JSONRPCBuilder.request(self._service_name, params, version = self._version, id = self._id)
        resp, content = self._http_client.request(self._url, "POST", post_data, headers = http_headers)
        if resp.status != 200:
            raise JSONRPCError(resp.reason)
        jsonrpc_data = None
        try:
            jsonrpc_data = jsonrpc_loads(content, self._version)
        except Exception, e:
            raise JSONRPCParseError("%s" % e)
        if jsonrpc_data['id'] == self._id:
            raise JSONRPCServerError('JSONRPC request id is `%s`, but response id is `%s`' % (self._id, jsonrpc_data['id']))
        if (jsonrpc_data["error"] != None):
            if jsonrpc_data["error"]["code"] in jsonrpc_error_map:
                err_cls = jsonrpc_error_map[jsonrpc_data["error"]["code"]](jsonrpc_data["error"]["message"],
                                                                               data =  jsonrpc_data["error"].get("data", None))
            else:
                err_cls = JSONRPCError(jsonrpc_data["error"]["message"], jsonrpc_data["error"]["code"],
                                       data = jsonrpc_data["error"].get("data", None))
            raise err_cls
        else:
            return jsonrpc_data["result"]

class JSONPProxy(object):
    """
    JSONP 代理 app，用于 ajax 跨域名的调用.

    `` 原理 ``

    如果 JSONPProxy 本身挂在 / 下面，那么如果客户端请求的 url 为 /path/to/other_app, 那么 JSONPProxy
    会代理请求该 url，并把返回封装成 JSONP 格式::

        callback_name(
            "将 response 转换成了 json 的数据"
        )

    然后返回给客户端.

    .. note::

        当代理失败，例如目标无响应或超时或返回一个非正常的状态码， JSONPProxy 则认为代理失败，会返回 502 Bad Gateway 错误

        如果发生超时，则同样返回 502 状态

        当请求 URL 中不包含 ``callback`` 指定的 GET 参数或参数无效则返回 400 Bad Request 错误

    .. seealso::

        googling for ``jQuery`` and ``JSONP``
    """

    def __init__(self, timeout = None, callback_name = None, encoding = "utf-8"):
        """
        :param timeout: socket 级的 timeout 设置
        :param callback: JQuery 附加在 GET 请求中的 callback 参数名， 默认为 ``_callback``
        """

        self._proxy_app = TransparentProxy(timeout = timeout)
        self._callback_name = callback_name or "_callback"
        # 502 Bad Gateway
        # The server, while acting as a gateway or proxy,
        # received an invalid response from the upstream server it accessed in attempting to fulfill the request.
        self._bad_gateway_app = HTTPStatus(502)
        # Bad Request
        # The request could not be understood by the server due to malformed syntax.
        # The client SHOULD NOT repeat the request without modifications.
        self._bad_request_app = HTTPStatus(400)
        self.encoding = encoding
        self.logger = logging.getLogger(__name__ + "." + self.__class__.__name__)

    def __call__(self, environ, start_response):
        if environ.get("SCRIPT_NAME", "") != "":
            new_environ = environ.copy()
            new_environ["SCRIPT_NAME"] = ""
        else:
            new_environ = environ
        req = Request(new_environ)
        if self._callback_name not in req.GET:
            self.logger.error("`callback` argument not be found in url querystring.")
            return self._bad_request_app(new_environ, start_response)
        callback = req.GET[self._callback_name]
        resp = None
        try:
            resp = req.get_response(self._proxy_app)
        except:
            url = construct_url(environ)
            self.logger.error("proxing '%s' failure." % url, exc_info = True)
            return self._bad_gateway_app(environ, start_response)
        if resp.status_int == 200:
            try:
                body = callback + "(" + simplejson.dumps(resp.body, encoding = self.encoding) + ")"
            except:
                url = construct_url(environ)
                self.logger.error("'%s' responses can't convert to json data." % url, exc_info = True)
                return self._bad_gateway_app(environ, start_response)
            else:
                resp.body = body
                # FIXME: text/javascript or application/x-javascript ?
                resp.content_type = "text/javascript; charset=" + self.encoding
        else:
            url = construct_url(environ)
            self.logger.error("'%s' returned an unknown status code %s." % (url, resp.status_int))
            return self._bad_gateway_app(environ, start_response)
        return resp(environ, start_response)

class JSONPMiddleware(object):
    """
    本中间件将被封装的 app 的返回结果封装成 JSONP 格式返回

    .. seealso::

        :class:`JSONPProxy`
    """

    DEFAULT_CALLBACK_FUNC = '_callback'

    def __init__( self, app, callback_name=DEFAULT_CALLBACK_FUNC ):
        self.app = app
        self._callback_name = callback_name
        # Bad Request
        # The request could not be understood by the server due to malformed syntax.
        # The client SHOULD NOT repeat the request without modifications.
        self._bad_request_app = status_map[400]()

    def __call__(self, environ, start_response):
        req = Request(environ)
        if self._callback_name not in req.GET:
            return self._bad_request_app(environ, start_response)
        callback = req.GET[self._callback_name]
        is_ok = []
        def repl_start_response(status, headers, exc_info=None):
            code = int(status.split(None, 1)[0])
            if code == 200:
                is_ok.append(None)
                return lambda x : None
            return start_response(status, headers, exc_info)
        body = self.app(environ, repl_start_response)
        try:
            body = callback + "(" + simplejson.dumps(body) + ")"
        except:
            body = callback + "()"
        resp = Response(body, content_type = "text/javascript; charset=utf-8")
        return resp(environ, start_response)

def make_jsonpproxy_app(global_conf, timeout = None, callback_name = None):
    """
    paste EGG Entry Point::

        jsonpproxy

    用 PasteDeploy 部署::

        [app:JSONPProxyApp]
        use = egg:khan#jsonpproxy
        # optional
        timeout = 10
        # optional, defaults is `_callback`
        callback_name = _callback

        [app:main]
        use = egg:paste#urlmap
        /jsonpproxy = JSONPProxyApp
    """

    timeout = timeout and int(timeout) or None
    app = JSONPProxy(timeout = timeout, callback_name = callback_name)
    return app

def make_jsonp_middleware(global_conf, callback_name = None):
    """
    paste EGG Entry Point::

        jsonp

    用 PasteDeploy 部署::

        [filter:JSONPMiddleware]
        use = egg:khan#jsonp
        # optional, defaults is `_callback`
        callback_name = _callback

        [app:main]
        use = egg:paste#test
        filter-with = JSONPMiddleware
    """

    def filter(app):
        return JSONPMiddleware(app, callback_name)
    return filter

def make_jsonrpc_client_object(global_conf, url, user=None, password=None, **keyword):
    """
    配置 JSONRPCClient

    paste EGG Entry Point::

        jsonrpc_client

    用 PasteDeploy 部署::

        [object:jsonrpc_client]
        use = egg:khan#jsonrpc_client
        url = http://localhost:7032
        user = admin
        password = 123456

        .. 其余被附加的参数将会填入 JSONRPCClient.__init__(... **keyword)

    .. seealso::

      JSONRPCClient

    """

    if not url:
        raise ValueError("url must be set")

    client = JSONRPCClient(url = url, **keyword)
    if user:
        client.add_credentials(user, password)
    return client

class JSONRPCClientCommand(Command):
    """
    Calling a json-rpc function and print the output.

    Example::

        $ paster khan.jsonrpc -s http://localhost:7032 group.create \\"new_group\\",[\\"new_permission\\"]

        $ paster khan.jsonrpc -s http://localhost:7032 group.list_all 1,100

        $ paster khan.jsonrpc -s http://localhost:7032 group.test 1,100 a=1,b=\\"2\\"

        $ paster khan.jsonrpc -s http://localhost:7032 -u admin -p 123 group.test
    """

    args_description = "method args kargs"

    min_args = 1

    max_args = 3

    parser = Command.standard_parser(simulate=True)

    parser.add_option('-s', '--service',
                      dest='service',
                      default="http://localhost",
                      help="the json-rpc service url [default: %default]")

    parser.add_option('-u', '--user',
                      dest='user',
                      default=None,
                      help=("Specifie user name"))

    parser.add_option('-p', '--password',
                      dest='password',
                      default=None, metavar="PWD",
                      help="Specifie password of the user [default: %default]")

    parser.add_option('-d', '--debug',
                      dest='debug', action='store_true',
                      help="debug mode [default: disabled]")

    def command(self):
        jc = JSONRPCClient(self.options.service)
        if self.options.user:
            jc.add_credentials(self.options.user, self.options.password or "")
        method = self.args[0]
        if len(self.args) > 1:
            method_args_str = self.args[1] + ","
        else:
            method_args_str = ""
        if len(self.args) > 2:
            method_kargs_str = self.args[2]
        else:
            method_kargs_str = ""
        sep_line = "-" * 70
        try:
            result = eval("jc." + method + "(*(" + method_args_str + "), **dict(" + method_kargs_str + "))")
        except JSONRPCError, e:
            print "Error:"
            print sep_line
            if self.options.debug:
                print traceback.print_exc()
            else:
                print repr(e)
            return EX_SOFTWARE
        except (SyntaxError, NameError):
            print "Error:"
            print sep_line
            if self.options.debug:
                print traceback.print_exc()
            else:
                print "`method` or `args` or `kargs` invalid. please run 'paster khan.jsonrpc --help' for detail."
            return EX_SOFTWARE
        except:
            print "Error:"
            print sep_line
            print traceback.print_exc()
            return EX_SOFTWARE
        else:
            print "Result:"
            print sep_line
            print result
            return EX_OK


