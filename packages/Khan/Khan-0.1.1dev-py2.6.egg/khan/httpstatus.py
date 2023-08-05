# -*- coding: utf-8 -*-

"""
HTTP 状态处理
=================================

本模块提供工具去处理 HTTP 状态.

索引
=================================

* :class:`HTTPStatus`
* :class:`HTTPStatusDispatcher`
* :func:`make_httpstatus_app`
* :func:`make_httpstatusdispatcher_middleware`

=================================

.. autoclass:: HTTPStatus
    :members: 
.. autoclass:: HTTPStatusDispatcher
    :members:
.. autofunction:: make_httpstatus_app
.. autofunction:: make_httpstatusdispatcher_middleware
"""

import logging
from UserDict import DictMixin
from webob import Response
from webob.exc import status_map
from paste.util.converters import asbool
from khan.deploy import loadapp

__all__ = ["HTTPStatus", "HTTPStatusDispatcher"]

class HTTPStatus(Response):
    """
    代表一个 http status 的 wsgi app, 派生自 ``webob.Response`` 
    
    实际上本类封装的是一个 ``paste.httpexceptions.HTTPException`` 子类的 app, 
    如果用户没有设置 `body` 或者 `app_iter` 属性，将使用封装的``paste.httpexceptions.HTTPException`` 
    子类的 body 来代替.
    
    .. note::
        
        对本类 status 属性赋值无效，因为 status 在本类初始化的时候已经指定.

    .. TODO::
        
        应该实现一个 status/status_int 方法，在用户尝试对 status/status_int 赋值的时候抛出异常
    """
    
    def __init__(self, code, *args, **kargs):
        """
        :param code: http 状态码
        :param args: 传递给 paste.httpexceptions.HTTPException 的构造函数参数.
        :param kargs: 传递给 paste.httpexceptions.HTTPException 的构造函数参数.
        
        :type code: int
        """
        
        code = int(code)
        assert code in status_map, ValueError("status code '%s' invalid." % code)
        self.code = code
        self._httpe = status_map[code](*args, **kargs)
        super(HTTPStatus, self).__init__()
        self.status_int = code

    def __call__(self, environ, start_response):
        orig_response = []
        def repl_start_response(status, headers, exc_info=None):
            orig_response[ : ] = status, headers
            return lambda x : None
        app_iter = self._httpe(environ, repl_start_response)
        if not self.body and ((not self.app_iter) or (not self.app_iter[0])):
            self.app_iter = app_iter
        if orig_response:
            self.status = orig_response[0]
            self.headerlist.extend(orig_response[1])
        return super(HTTPStatus, self).__call__(environ, start_response)
        
def make_httpstatus_app(global_conf, status, **httpexception_options):
    """
    Paste EGG entry point::
        
        httpstatus
        
    PasteDeploy example::
    
        [app:HTTPStatus]
        use = egg:khan#httpstatus
        status = 404
        
        [app:urlmap]
        /a =  HTTPStatus
    """
    
    return HTTPStatus(status, **httpexception_options)

class HTTPStatusDispatcher(DictMixin, object):
    """
    基于 HTTP 状态的 WSGI app 转发, 转发请求给 app 之前，本中间件会设置::
        
        environ["khan.httpstatusdispatcher.orig_status"] = 原始 http status
        environ["khan.httpstatusdispatcher.orig_headers"] = 原始 http headers
    
    本类实现 Dict 接口，使用示例::
    
        app = HTTPStatusDispatcher(app)
        app[404] = HTTPStatus(404)
        app[401] = HTTPStatus(401)
    """
    
    ORIG_STATUS_KEY = "khan.httpstatusdispatcher.orig_status"
    ORIG_HEADERS_KEY = "khan.httpstatusdispatcher.orig_headers"
    
    def __init__(self, app, keep_status = True):
        """
        :param app: wsgi app.
        :param keep_status: 是否总是使用原始 app 的 response 的 status 和 headers 来作为最终返回的 status 和 headers.
        
        :type keep_status: bool
        """
        
        self._app = app
        self._map = {}
        self._keep_status = keep_status
        self._logger = logging.getLogger(self.__class__.__name__)
        
    def __getitem__(self, code):
        return self._map[code]
    
    def __setitem__(self, code, app):
        self._map[int(code)] = app
    
    def __delitem__(self, code):
        del self._map[code]
    
    def keys(self):
        return self._map.keys()
    
    def __call__(self, environ, start_response):
        is_caught = []
        orig_response = []
        def repl_start_response(status, headers, exc_info=None):
            code = int(status.split(None, 1)[0])
            if code in self._map:
                orig_response[ : ] = status, headers
                is_caught.append(code)
                return lambda x : None
            else:
                return start_response(status, headers, exc_info)
        resp = self._app(environ, repl_start_response)
        if is_caught:
            orig_status, orig_headers = orig_response
            environ[self.ORIG_STATUS_KEY] = orig_status
            environ[self.ORIG_HEADERS_KEY] = orig_headers
            matched_app = self._map[is_caught[0]]
            if self._keep_status:
                self._logger.debug("caught '%s' status, dispatch request to app %r, and kept response status." 
                                   % (is_caught[0], matched_app))
                def new_start_response(status, headers, exc_info=None):
                    return start_response(orig_status, orig_headers + headers, exc_info)
                return matched_app(environ, new_start_response)
            else:
                self._logger.debug("caught '%s' status, dispatch request to app %r." 
                                   % (is_caught[0], matched_app))
                return matched_app(environ, start_response)
        else:
            return resp

def make_httpstatusdispatcher_middleware(global_conf, keep_status=True, conf=None, **maps):
    """
    Paste EGG entry point::
        
        statusdispatcher
        
    PasteDeploy example::
    
        [app:main]
        use = egg:khan#status
        status = 404
        filter-with = statusdispatcher
        
        [app:file]
        use = egg:khan#file
        file = /home/alec/kk.py
        
        [filter:statusdispatcher]
        use = egg:khan#statusdispatcher
        keep_status = False
        404 = file
        403 401 500 = file
    """
    
    def middleware(app):
        config_file = conf or global_conf["__file__"]
        dispatcher = HTTPStatusDispatcher(app, asbool(keep_status))
        for status_code, app_name in maps.iteritems():
            if " " in status_code:
                handle_app = loadapp("config:" + config_file, app_name, global_conf)
                status_codes = status_code.strip().split()
                status_codes = map(lambda item : item.strip(), status_codes)
                status_codes = filter(lambda item : item, status_codes)
                status_codes = map(lambda item : int(item), status_codes)
                for c in status_codes:
                    dispatcher[c] = handle_app
            else:
                status_code = int(status_code)
                handle_app = loadapp("config:" + config_file, app_name, global_conf)
                dispatcher[status_code] = handle_app
        return dispatcher
    return middleware
