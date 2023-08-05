# -*- coding: utf-8 -*-

"""
会话管理(Session)
=================================

本模块提供工具去管理请求期间的用户会话(Session).

索引
=================================

* :attr:`session`
* :class:`SessionContainer`
* :class:`ISessionIdentifier`
* :class:`CookieIdentifier`
* :class:`HTTPHeaderIdentifier`
* :class:`SessionMiddleware`
* :func:`make_session_middleware`
* :func:`make_cookie_identifier_plugin`
* :func:`make_httpheader_identifier_plugin`

=================================

.. attribute:: session
    
    该变量在 :class:`SessionMiddleware` 中间件接收到请求的时候注册并可用.

.. autoclass:: SessionContainer
.. autoclass:: ISessionIdentifier
.. autoclass:: CookieIdentifier
.. autoclass:: HTTPHeaderIdentifier
.. autoclass:: SessionMiddleware
.. autofunction:: make_session_middleware
.. autofunction:: make_cookie_identifier_plugin
.. autofunction:: make_httpheader_identifier_plugin
"""

import logging, time
from UserDict import DictMixin
from webob import Request, Response
from zope.interface import Interface, implements
from paste.registry import StackedObjectProxy, RegistryManager
from paste.util.converters import asbool
from khan.utils import requestTypes, request_classifier, isiterable, unique_id
from khan.store import get_backend
from khan.deploy import loadobject
from khan.urlparse import get_wild_domain, remove_port_from_domain

__all__ = [
   "session", 
   "SessionContainer", 
   "ISessionIdentifier", 
   "SessionMiddleware", 
   "HTTPHeaderIdentifier", 
   "CookieIdentifier"
]

session = StackedObjectProxy(None, name="session")

class SessionContainer(DictMixin):
    """
    会话容器，用于存储一个用户会话期间的数据，本容器实现 dict 接口.
    所有数据的更改都必须调用 :meth:`save` 方法之后才生效.
    
    :data id: session id
    """
    
    @staticmethod
    def create(store, expires = None):
        """
        助手函数，用于建立一个 :class:`SessionContainer` 实例
        
        :param store: dict like object
        :param expires: 过期时间
        
        :rtype: :class:`SessionContainer`
        """
        
        sid = unique_id()
        return SessionContainer(sid, store, expires)
    
    def __init__(self, sid, store, expires = None):
        """
        :param sid: session id, 该值应该用 :func:`unique_id` 函数建立
        :param store: 实现了 dict 接口的对象，该对象将作为存储数据的介质, 
        :param expires: session 过期时间(秒), 默认为 600 (10 分钟)
        
        :type sid: string
        :type store: dict like object
        :type expires: int or None
        """
        
        self._store = store
        self._expires = expires and int(expires) or 600
        if sid in self._store:
            try:
                exp, value = self._store[sid]
            except TypeError:
                # 值不是一个 tuple(exp, value)
                del self._store[sid]
                self._data = {}
            else:
                # Delete if item timed out.
                if exp < time.time():
                    del self._store[sid]
                    self._data = {}
                else:
                    self._data = value
                    exp = time.time() + self._expires
                    self._store[sid] = (exp, value) 
        else:
            self._data = {}
        self.created = False
        self.id = sid

    def __setitem__(self, key, value):
        self._data[key] = value
    
    def __getitem__(self, key):
        return self._data[key]
    
    def __delitem__(self, key):
        del self._data[key]
    
    def __contains__(self, key):
        return key in self._data
     
    def keys(self):
        return self._data.keys()
    
    def save(self):
        """
        保存session数据，并写入存储介质
        """
        
        exp = time.time() + self._expires
        self._store[self.id] = (exp, self._data) 
        self.created = True
        try:
            # store 一般为一个 shove store，这里尝试调用 shove store 的 sync 方法将数据写入store内部的存储介质内.
            self._store.sync()
        except AttributeError:
            pass
        
class ISessionIdentifier(Interface):
    """
    Session ID 获取和写入接口， 被 :class:`SessionMiddleware` 用于从用户请求中获得 session 标识(sid) 
    和保存用户 session 标识到客户端
    """
    
    def identify(self, req):
        """
        从用户请求中获得 session 标识(sid)
        
        :param environ: wsgi environ
        :type environ: dict
        
        :rtype: string
        """
        
        pass

    def remember(self, resp, session):
        """
        保存用户 session 标识到客户端, 本函数的默认行为是什么都不做
        
        :param resp: webob.Response
        :param session: 用户 session
        
        :type resp: webob.Response
        :type session: :class:`SessionContainer`
        """
        
        pass
    
class CookieIdentifier(object):
    """
    用 Cookie 保存 session id
        
    .. seealso:: 
    
        :class:`ISessionIdentifier`, :class:`SessionMiddleware`, :class:`HTTPHeaderIdentifier`
    """
    
    implements(ISessionIdentifier)
    
    COOKIE_NAME = "X-Kh-Sid"
    
    def __init__(self, name = COOKIE_NAME, max_age = None, path = "/", domain = None, secure = False):
        self._cookie_name = name
        self._cookie_max_age = max_age
        self._cookie_path = path
        self._cookie_domain = domain
        self._cookie_secure = secure
        self._logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
    
    def decide(self, req):
        return requestTypes.BROWSER == request_classifier(req.environ)
    
    def identify(self, req):
        if not self.decide(req):
            return 
        if self._cookie_name in req.cookies:
            self._logger.debug("get session identify from cookie '%s'." % self._cookie_name)
            return req.cookies[self._cookie_name]
    
    def remember(self, resp, session):
        if not self.decide(resp.request):
            return resp
        if session.created:
            self._logger.debug("write session identify to cookie '%s'." % self._cookie_name)
            if self._cookie_domain is None:
                cur_domain = resp.request.environ.get("HTTP_HOST", resp.request.environ.get("SERVER_NAME"))
                cur_domain = remove_port_from_domain(cur_domain)
                wild_domain = get_wild_domain(cur_domain)
                resp.set_cookie(self._cookie_name, session.id, max_age = self._cookie_max_age, 
                               path = self._cookie_path, secure = self._cookie_secure)
                resp.set_cookie(self._cookie_name, session.id, max_age = self._cookie_max_age, 
                               path = self._cookie_path, domain = cur_domain, secure = self._cookie_secure)
                resp.set_cookie(self._cookie_name, session.id, max_age = self._cookie_max_age, 
                               path = self._cookie_path, domain = wild_domain, secure = self._cookie_secure)
            else:
                resp.set_cookie(self._cookie_name, session.id, max_age = self._cookie_max_age, 
                               path = self._cookie_path, domain = self._cookie_domain, secure = self._cookie_secure)
        return resp
    
def make_cookie_identifier_plugin(global_conf, name = CookieIdentifier.COOKIE_NAME, 
                                  max_age = None, path = "/", domain = None, secure = False):
    """
    Paste EGG entry point::
        
        session.cookie
        
    PasteDeploy example::

        [filter:session]
        use = egg:khan#session
        identifiers = cookie
        
        [object:cookie]
        use = egg:khan#session.cookie
        name = X-Kh-Sid
        domain = .domain.com
        path = /
        max_age = 124000
    
    .. seealso:: 
    
        :class:`CookieIdentifier`, :class:`SessionMiddleware`
    """
    
    secure = asbool(secure)
    if max_age:
        max_age = int(max_age)
    return CookieIdentifier(name = name, max_age = max_age, path = path, domain = domain, secure = secure)
 
class HTTPHeaderIdentifier(object):
    
    """
    用 HTTP header 保存 session id
    
    .. seealso:: 
    
        :class:`ISessionIdentifier`, :class:`SessionMiddleware`, :class:`CookieIdentifier`
    """
    
    implements(ISessionIdentifier)
    
    HEADER_NAME = "X-Kh-Sid"
    
    def __init__(self, name = HEADER_NAME):
        self._field_name = name
        self._logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
        
    def identify(self, req):
        if self._field_name in req.headers:
            self._logger.debug("get session identify from http header '%s'." % self._field_name)
            return req.headers[self._field_name]
    
    def remember(self, resp, session):
        if session.created:
            self._logger.debug("write session identify to http header '%s'." % self._field_name)
            resp.headers[self._field_name] = session.id
        return resp
    
def make_httpheader_identifier_plugin(global_conf, name = HTTPHeaderIdentifier.HEADER_NAME):
    """
    Paste EGG entry point::
        
        session.header
        
    PasteDeploy example::

        [filter:session]
        use = egg:khan#session
        identifiers = header
        
        [object:header]
        use = egg:khan#session.header
        name = X-Kh-Sid
    
    .. seealso:: 
    
        :class:`HTTPHeaderIdentifier`, :class:`SessionMiddleware`
    """
    
    
    return HTTPHeaderIdentifier(name)

class RequestParamIdentifier(object):
    
    """
    用 request params 保存 session id, 专门用来对付无 Cookie 会话问题
    
    .. seealso:: 
    
        :class:`ISessionIdentifier`, :class:`SessionMiddleware`, :class:`CookieIdentifier`
    """
    
    implements(ISessionIdentifier)
    
    FIELD_NAME = 'X-Kh-Sid'
    
    def __init__(self, name = None):
        self._field_name = name or RequestParamIdentifier.FIELD_NAME
        self._logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
        
    def identify(self, req):
        if self._field_name in req.params:
            self._logger.debug("get session identify from request params(%s) '%s'." % (req.method, self._field_name))
            return req.params[self._field_name]
    
    def remember(self, resp, session):
        return resp

def make_request_param_identifier_plugin(global_conf, name = None):
    """
    Paste EGG entry point::
        
        session.req_param
        
    PasteDeploy example::

        [filter:session]
        use = egg:khan#session
        identifiers = req_param
        
        [object:req_param]
        use = egg:khan#session.req_param
        name = X-Kh-Sid
    
    .. seealso:: 
    
        :class:`HTTPHeaderIdentifier`, :class:`SessionMiddleware`
    """
    return RequestParamIdentifier(name)

class SessionMiddleware(object):
    """
    Session 中间件，在 app 处理请求前本中间件会注册一个 :data:`session` (:class:`SessionContainer` 实例)  全局变量，
    该变量在请求期间可用. 
    """
    
    ENVIRON_KEY = "khan.session"
    
    def __init__(self, app, store = None, identifiers = None, expires = None):
        """
        :param app: wsgi app
        :param store: session 数据的存储介质, 默认用 "memory://"
        :param identifiers: 一个 :class:`ISessionIdentifier` 对象列表, 默认为 [:class:`CookieIdentifier`]
        :param expires: session 过期时间，默认为 600 秒(10分钟)
        
        :type store: dict like object
        :type identifiers: list
        :type expires: int or None
        """
        
        if identifiers:
            if not isiterable(identifiers):
                identifiers = [identifiers]
        else:
            identifiers = [CookieIdentifier()]
        self._identifiers = identifiers
        self._app = app
        self._wapper_app = RegistryManager(self._wapper_call)
        if store is None:
            store = get_backend("memory://")
        self._store = store
        self._expires = expires
        self._logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
    
    def _wapper_call(self, environ, start_response):
        req = Request(environ)
        sid = None
        for identifier in self._identifiers:
            if identifier is None:
                continue

            identify = identifier.identify(req)
            if identify:
                sid = identify.strip()
                break
        if not sid:
            sess = SessionContainer.create(self._store, expires = self._expires)
        else:
            if sid in self._store:
                sess = SessionContainer(sid, self._store, expires = self._expires)
            else:
                self._logger.debug("sid '%s' not in store." % sid)
                sess = SessionContainer.create(self._store, expires = self._expires)

        reg = environ["paste.registry"]
        reg.register(session, sess)
        orig_resp_data = []
        def repl_start_response(status, headers, exc_info=None):
            orig_resp_data[ : ] = status, headers
            return lambda x : None
        resp_body = self._app(environ, repl_start_response)
        resp = Response("".join(resp_body), status = orig_resp_data[0], headerlist = orig_resp_data[1], request = req)
        if sess.created:
            for identifier in self._identifiers:
                resp = identifier.remember(resp, sess)
                
        return resp(environ, start_response)
    
    def __call__(self, environ, start_response):
        if self.ENVIRON_KEY in environ:
            self._logger.debug("`%s` exists." % self.__class__.__name__)
            return self._app(environ, start_response)
        else:
            environ[self.ENVIRON_KEY] = self
            return self._wapper_app(environ, start_response)

def make_session_middleware(global_conf, store = None, expires = None, 
                            identifiers = None, conf = None):
    """
    Paste EGG entry point::
        
        session
        
    PasteDeploy example::
    
        [app:sessionstore]
        use = egg:khan#rpcstore
        store = dbm://session.db
        
        [filter:session]
        use = egg:khan#session
        expires = 600
        store = store
        identifiers = cookie header
        
        [object:store]
        use = egg:khan#store
        uri = khan.rpc://localhost:7040
        cache = memory://
        rpc_timeout = 30
        
        [object:cookie]
        use = egg:khan#session.cookie
        name = X-Kh-Sid
        domain = .domain.com
        path = /
        max_age = 124000
        
        [object:header]
        use = egg:khan#session.header
        name = X-Kh-Sid
    
    .. seealso:: 
        
        关于 store 请看 :mod:`khan.store`
    
    .. seealso::
        
        :class:`SessionMiddleware`
    """
    
    conf = conf or global_conf["__file__"]
    expires = expires and int(expires) or None
    identifier_plugins = []
    if identifiers:
        for identifier_name in identifiers.split():
            # FIXME
            identifier_plugins.append(loadobject("config:%s" % conf, identifier_name, global_conf))

    if store:
        if "://" in store:
            store = get_backend(store)
        else:
            store = loadobject("config:%s" % conf, store, global_conf)
    def middleware(app):
        return SessionMiddleware(app, store, identifier_plugins, expires = expires)
    return middleware

class TesterIdentifier(object):
    
    implements(ISessionIdentifier)
    
    session_id = None
    
    def __init__(self):
        self._logger = logging.getLogger(__name__ + "." + self.__class__.__name__)
        
    def identify(self, req):
        self._logger.debug("identify session id: %s" % self.session_id)
        return self.session_id
    
    def remember(self, resp, session):
        if session.created:
            self.session_id = session.id
        else:
            self.session_id = None
        self._logger.debug("remember session id: %s" % self.session_id)
        
