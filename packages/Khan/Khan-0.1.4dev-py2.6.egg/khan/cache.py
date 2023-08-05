# -*- coding: utf-8 -*-

"""
缓存
=================================

本模块提供工具去缓存数据.

索引
=================================

* :class:`CacheContainer`
* :func:`cached`
* :func:`make_cache_middleware`

=================================

.. autoclass:: CacheContainer
.. autofunction:: cached
.. autofunction:: make_cache_middleware
"""

import time, logging
from rfc822 import formatdate
from UserDict import DictMixin
from webob import Response
from webob.exc import status_map
from khan.store import get_backend
from khan.utils import get_request_handler_name, unique_id
from khan.utils.decorator import update_wrapper_for_handler

__all__ = ["cached", "CacheContainer", "etag_cached"]

log = logging.getLogger(__name__)

DEFAULT_EXPIRES = 300

CATCH_ALL_STATUS = None

CACHE_ALL_HEADERS = None 

def cached(container = None, expires = DEFAULT_EXPIRES, catch_status = CATCH_ALL_STATUS, 
           exclude_headers = CACHE_ALL_HEADERS):
    """
    缓存 decorator, 该 decorator 用于缓存 wsgi app 或者 webob request handler 的返回结果.
    
    :param container: cache container
    :param expires: 如果为 None 则永不过期
    :param catch_status: 要捕获的 http 状态码，只有匹配的状态码才会被缓存
    :param exclude_headers: 不缓存的 http headers
    
    .. note::
        
        使用该 decorator 必须首先启用 :class:`CacheMiddleware` 中间件
    
    实例::
        
        @cached(container)
        def my_func(req):
            return webob.Response("body")
    
    .. seealso::
        
        :class:`CacheContainer`
    """
    
    if exclude_headers != CACHE_ALL_HEADERS:
        # 剔除重复项
        exclude_headers = set(exclude_headers)
    if container is None:
        container = CacheContainer(default_expires = expires)
    def decorator(handler):
        def wrapper(*args, **kargs):
            new_args = list(args)
            new_args.extend(kargs.values())
            if hasattr(handler, "_cache_key"):
                cache_key = handler._cache_key
            else:
                # 生成一个唯一的 key 作为 cache key 
                cache_key = unique_id()
                handler.__dict__["_cache_key"] = cache_key
            handler_name = get_request_handler_name(handler)
            if cache_key in container:
                status, headers, app_iter = container[cache_key]
                log.debug("restored the handler '%s' result from cache" % handler_name)
                if exclude_headers != CACHE_ALL_HEADERS:
                    headers = filter(lambda header : header[0].lower() not in exclude_headers, headers)
                resp = Response(status = status, app_iter = app_iter)
                resp.headerlist.extend(headers)
                # webob handler
                if len(args) == 1:
                    return resp
                # wsgi app
                else:
                    return resp(*args, **kargs)
            else:
                # webob handler
                if len(new_args) == 1:
                    resp = handler(*args, **kargs)
                    if catch_status == CATCH_ALL_STATUS or resp.status_int in catch_status:
                        log.debug("handler `%r` returned status code '%s', cache it." % (handler, resp.status_int))
                        headers = []
                        headers.extend(resp.headers)
                        data = (resp.status, headers, resp.app_iter)
                        container.set_value(cache_key, data, expires)
                    else:
                        log.debug("handler `%r` returned a unknown status code '%s', don't cache it."
                                        % (handler, resp.status_int))
                    return resp
                # wsgi app
                elif len(new_args) == 2:
                    environ, start_response = new_args
                    orig_response = []
                    def repl_start_response(status, headers, exc_info=None):
                        orig_response[ : ] = status, headers
                        lambda x : None
                    app_iter = handler(environ, repl_start_response)
                    if orig_response:
                        status_int = int(orig_response[0].split(None, 1)[0])
                        if catch_status == CATCH_ALL_STATUS or status_int in catch_status:
                            log.debug("handler `%r` returned status code '%s', cache it." % (handler, status_int))
                            data = (orig_response[0], orig_response[1], app_iter)
                            container.set_value(cache_key, data, expires)
                        else:
                            log.debug("handler `%r` returned a unknown status code '%s', don't cache it."
                                        % (handler, status_int))
                        start_response(orig_response[0], orig_response[1])
                        return app_iter
                    else:
                        raise TypeError("handler '%s' not to call the `start_response()`." % handler_name)
                else:
                    raise ValueError("`handler` invalid")
        return update_wrapper_for_handler(wrapper, handler)
    return decorator

def make_cache_middleware(global_conf, store = None, expires = DEFAULT_EXPIRES, 
                          catch_status = CATCH_ALL_STATUS, 
                          exclude_headers = CACHE_ALL_HEADERS):
    """
    make cache middleware.
    
    Paste EGG entry point::
        
        cache
        
    PasteDeploy example::
        
        [filter-app:cache]
        use = egg:khan#cache
        next = test
        store = dbm:///path/to/my.db
        expires = 300
        catch_status = 200 403 401
        exclude_headers = Khan-X-A Khan-X-B
        
        [app:test]
        use = egg:paste#test
    
    .. seealso::
        
        :func:`cached`
    """
    
    def middleware(app):
        if store:
            store = get_backend(store)
        expires = int(expires)
        if exclude_headers != CACHE_ALL_HEADERS:
            exclude_headers =  set(exclude_headers.split())
        if catch_status != CATCH_ALL_STATUS:
            catch_status = set(map(lambda status_str : int(status_str), catch_status.split()))
        return cached(CacheContainer(store), expires = expires, 
                      catch_status = catch_status, exclude_headers = exclude_headers)(app)
    return middleware

class CacheContainer(DictMixin, object):
    """
    本类被 :class:`CacheMiddleware` 用于存储缓存数据
    """
    
    def __init__(self, store = None, default_expires = DEFAULT_EXPIRES):
        """
        :param store: 实现了 dict 接口的对象 
        :param default_expires: 如果为 None 则永不过期
        """
        
        if store is None:
            store = get_backend("memory://")
        self._store = store
        self._expires = default_expires
        self._logger = logging.getLogger(self.__class__.__name__)
        
    def __getitem__(self, key):
        try:
            exp, value = self._store[key]
        except TypeError:
            # 值不是一个 tuple(exp, value)
            del self._store[key]
            raise KeyError('%s' % key)
        else:
            if exp is not None:
                # Delete if item timed out.
                if exp < time.time():
                    del self._store[key]
                    raise KeyError('%s' % key)
            return value
    
    def __setitem__(self, key, value):
        if self._expires is not None:
            # Set expiration time and value
            exp = time.time() + self._expires
        else:
            exp = None
        self._store[key] = (exp, value) 
    
    def __delitem__(self, key):
        del self._store[key]
    
    def keys(self):
        keys = []
        for key in self._store.keys():
            exp = self._store[key][0]
            if exp is not None:
                # Delete if item timed out.
                if exp < time.time():
                    del self._store[key]
                else:
                    keys.append(key)
            else:
                keys.append(key)
        return keys
    
    def clear(self):
        self._store.clear()
        
    def set_value(self, key, value, expires = DEFAULT_EXPIRES):
        if expires is None:
            exp = None
        else:
            # Set expiration time and value
            exp = time.time() + expires
        self._store[key] = (exp, value) 
    
    def get_value(self, key, create_func, expires = DEFAULT_EXPIRES):
        """
        根据一个 key 从缓存内取得一个值，如果该 key 不存在，
        则调用 ``create_func`` 函数来生成内容并存储该内容到缓存中并返回.
        
        :param key: 缓存 key
        :param create_func: 一个用于生成缓存内容的函数或 callable object.
        :param expires: 如果 expires 为 None 则永不过期
        
        :type key: string
        :type create_func: callable object
        :type expires: int or None
        
        :rtype: unknown
        """
        
        if self.__contains__(key):
            self._logger.debug("get value from cache store for key '%s'" % key)
            return self.__getitem__(key)
        else:
            self._logger.debug("created value and save to cache store for key '%s'" % key)
            try:
                value = create_func()
            except:
                self._logger.error("%r raised exception, returned `None`" % create_func, exc_info = True)
                return None
            self.set_value(key, value, expires)
            return value

_ETAG_CACHED_DECORATOR_KEY = "_khan_etag_cached"

def _set_etag_for_handler(handler, key, is_wsgiapp, new_args, last_modified = None):
    """
    this function used by :func:`etag_cached` internal
    """
    
    if is_wsgiapp:
        def repl_start_response(status, headers, exc_info=None):
            start_response = new_args[1]
            headers.append(("ETag", key))
            if last_modified:
                headers.append(("Last-Modified", formatdate(last_modified)))
            return start_response(status, headers, exc_info)
        return handler(new_args[0], repl_start_response)
    else:
        resp = handler(new_args[0])
        resp.headerlist.append(("ETag", key))
        if last_modified:
            resp.last_modified = last_modified
        return resp

def etag_cached(expires = None, key = None):
    """Use the HTTP Entity Tag cache for Browser side caching
    
    If a "If-None-Match" header is found, and equivilant to ``key``,
    then a ``304`` HTTP message will be returned with the ETag to tell
    the browser that it should use its current cache of the page.
    
    Otherwise, the ETag header will be added to the response headers.
    
    Example::
        
        @etag_cached(100)
        def app(environ, start_response):
            pass
    """
    
    def decorator(handler):
        if _ETAG_CACHED_DECORATOR_KEY in handler.__dict__:
            del handler.__dict__[_ETAG_CACHED_DECORATOR_KEY]
        def wrapper(*args, **kargs):
            """Wrapper for restrict"""
            new_args = list(args)
            new_args.extend(kargs.values())
            # wsgi app
            if len(new_args) == 2:
                environ = new_args[0]
                is_wsgiapp = True
            # webob handler
            elif len(new_args) == 1:
                environ = new_args[0].environ
                is_wsgiapp = False
            else:
                raise ValueError("`handler` invalid")
            if_none_match = environ.get('HTTP_IF_NONE_MATCH', None)
            if if_none_match is None:
                log.debug("ETag not in request, no cache")
                if not hasattr(handler, _ETAG_CACHED_DECORATOR_KEY):
                    mtime = time.time()
                    key1 = key or unique_id()
                    handler.__dict__[_ETAG_CACHED_DECORATOR_KEY] = (key1, mtime)
                else:
                    handler.__dict__[_ETAG_CACHED_DECORATOR_KEY][1] = time.time()
                return _set_etag_for_handler(handler, key1, is_wsgiapp, new_args, mtime)
            else:
                if not hasattr(handler, _ETAG_CACHED_DECORATOR_KEY):
                    log.debug("ETag didn't match, returning response object")
                    key1 = key or unique_id()
                    mtime = time.time()
                    handler.__dict__[_ETAG_CACHED_DECORATOR_KEY] = (key1, mtime)
                    return _set_etag_for_handler(handler, key1, is_wsgiapp, new_args, mtime)
                else:
                    key1, mtime = getattr(handler, _ETAG_CACHED_DECORATOR_KEY)
                    
                    # TODO: 应该处理用户传进来的 key 和函数内保存的 key 属性不同的情况
                    
                    if str(key1) == if_none_match:
                        if expires:
                            cur_time = time.time()
                            # 缓存已经超过限时
                            if (cur_time - mtime) >= expires:
                                log.debug("ETag didn't match, returning response object")
                                return _set_etag_for_handler(handler, key1, is_wsgiapp, new_args, cur_time)
                            # 缓存还未超过限时，直接返回 304 not modified
                            else:
                                log.debug("ETag match, returning 304 HTTP Not Modified Response")
                                resp = status_map[304]()
                                if is_wsgiapp:
                                    return resp(*args, **kargs)
                                else:
                                    return resp
                        # 如果 expires 设置为永远不到期
                        else: 
                            log.debug("ETag match, returning 304 HTTP Not Modified Response")
                            resp = status_map[304]()
                            if is_wsgiapp:
                                return resp(*args, **kargs)
                            else:
                                return resp
                    else:
                        log.debug("ETag didn't match, returning response object")
                        return _set_etag_for_handler(handler, key1, is_wsgiapp, new_args, time.time())
        return update_wrapper_for_handler(wrapper, handler)
    return decorator
    