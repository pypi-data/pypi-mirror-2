# -*- coding: utf-8 -*-
#
# (c) 2005 Ian Bicking and contributors; written for Paste (http://pythonpaste.org)
# Licensed under the MIT license: http://www.opensource.org/licenses/mit-license.php

"""
代理
=================================
An application that proxies WSGI requests to a remote server.

TODO:

* Send ``Via`` header?  It's not clear to me this is a Via in the
  style of a typical proxy.

* Other headers or metadata?  I put in X-Forwarded-For, but that's it.

* Signed data of non-HTTP keys?  This would be for things like
  REMOTE_USER.

* Something to indicate what the original URL was?  The original host,
  scheme, and base path.

* Rewriting ``Location`` headers?  mod_proxy does this.

* Rewriting body?  (Probably not on this one -- that can be done with
  a different middleware that wraps this middleware)

索引
=================================

* :class:`Proxy`
* :class:`TransparentProxy`
* :func:`make_proxy_app`
* :func:`make_transparent_proxy_app`

=================================

.. autoclass:: Proxy
.. autoclass:: TransparentProxy
.. autofunction:: make_proxy_app
.. autofunction:: make_transparent_proxy_app
"""

from __future__ import absolute_import
import urlparse, urllib, logging
import httplib2
from paste import httpexceptions
from paste.util.converters import aslist
from khan.httpstatus import HTTPStatus

__all__ = ["Proxy", "TransparentProxy"]

# Remove these headers from response (specify lower case header
# names):
filtered_headers = (     
    'transfer-encoding',
    'connection',
    'keep-alive',
    'proxy-authenticate',
    'proxy-authorization',
    'te',
    'trailers',
    'upgrade',
    "status",
    # FIXME: 该头被 httplib2 加入, 但在 webtest/lint 里会报错, 因为此头不合法, 仍为解决, 只能在这里把它过滤掉
    "-content-encoding"
)

def filter_res_headers(headers):
    headers_out = []
    for header, value in headers.items():
        if header.lower() not in filtered_headers:
            headers_out.append((header, value))
    return headers_out

class Proxy(object):
    """
    一个代理 app， 改良自 ``paste.proxy.Proxy``.
    
    本 app 使用 httplib2 作为底层 http client 实现, 以便实现请求超时.
    
    如果找不到服务器则返回 404 状态
    
    如果 httplib2 在请求期间抛出异常将一律返回 502 状态 (502 Bad Gateway)
    """
    
    def __init__(self, address, cache = None, timeout = None, allowed_request_methods=(), suppress_http_headers=()):
        """
        :param address: the full URL ending with a trailing ``/``
        :param cache: The cache parameter is either the name of a directory to be used as a flat file cache, 
            or it must an object that implements the required caching interface (like ``httplib2.FileCache``)
        :param timeout: The timeout parameter is the socket level timeout
        :param allowed_request_methods: list of request methods
        :param suppress_http_headers:
            list of http headers (lower case, without
            the leading ``http_``) that should not be passed on to target host
        """
        
        self.address = address
        self.parsed = urlparse.urlsplit(address)
        self.scheme = self.parsed[0].lower()
        assert self.scheme in ["http", "https"], ValueError("`address` invalid")
        self.host = self.parsed[1]
        self.path = self.parsed[2]
        self.allowed_request_methods = [x.lower() for x in allowed_request_methods if x]
        self.suppress_http_headers = [x.lower() for x in suppress_http_headers if x]
        self.http = httplib2.Http(cache = cache, timeout = timeout)
        # 502 Bad Gateway
        # The server, while acting as a gateway or proxy, 
        # received an invalid response from the upstream server it accessed in attempting to fulfill the request. 
        self._bad_gateway_app = HTTPStatus(502)
        self._not_found_app = HTTPStatus(404)
        self._logger = logging.getLogger(self.__class__.__name__)
        
    def __call__(self, environ, start_response):
        if (self.allowed_request_methods and 
            environ['REQUEST_METHOD'].lower() not in self.allowed_request_methods):
            return httpexceptions.HTTPBadRequest("Disallowed")(environ, start_response)
        headers = {}
        for key, value in environ.items():
            if key.startswith('HTTP_'):
                key = key[5:].lower().replace('_', '-')
                if key == 'host' or key in self.suppress_http_headers:
                    continue
                headers[key] = value
        #headers['host'] = self.host
        if 'host' in headers:
            del headers['host']
        if 'REMOTE_ADDR' in environ:
            headers['x-forwarded-for'] = environ['REMOTE_ADDR']
        if environ.get('CONTENT_TYPE'):
            headers['content-type'] = environ['CONTENT_TYPE']
        if environ.get('CONTENT_LENGTH'):
            if environ['CONTENT_LENGTH'] == '-1':
                # This is a special case, where the content length is basically undetermined
                body = environ['wsgi.input'].read(-1)
                headers['content-length'] = str(len(body))
            else:
                headers['content-length'] = environ['CONTENT_LENGTH'] 
                length = int(environ['CONTENT_LENGTH'])
                body = environ['wsgi.input'].read(length)
        else:
            body = ''
            
        path_info = urllib.quote(environ['PATH_INFO'])
        if self.path:            
            request_path = path_info
            if request_path and request_path[0] == '/':
                request_path = request_path[1:]
            path = urlparse.urljoin(self.path, request_path)
        else:
            path = path_info
        if environ.get('QUERY_STRING'):
            path += '?' + environ['QUERY_STRING']
        path = self.scheme + "://" + self.host + path
        try:
            res, res_body = self.http.request(path, environ['REQUEST_METHOD'], body, headers)
        except httplib2.ServerNotFoundError:
            return self._not_found_app(environ, start_response)
        except:
            self._logger.error("proxy request fail.", exc_info = True)
            return self._bad_gateway_app(environ, start_response)
        headers_out = filter_res_headers(res)
        status = '%s %s' % (res.status, res.reason)
        start_response(status, headers_out)
        return [res_body]

def make_proxy_app(global_conf, address, timeout = 30, allowed_request_methods="", suppress_http_headers=""):
    """
    Make a WSGI application that proxies to another address:
    
    ``address``
        the full URL ending with a trailing ``/``
        
    ``allowed_request_methods``:
        a space seperated list of request methods (e.g., ``GET POST``)
        
    ``suppress_http_headers``
        a space seperated list of http headers (lower case, without
        the leading ``http_``) that should not be passed on to target
        host
        
    paste EGG Entry Point::
        
        proxy
        
    用 PasteDeploy 部署::
        
        [app:proxy]
        use = egg:khan#proxy
        address = http://www.baidu.com
        timeout = 30
        
    .. seealso::
        
        :class:`Proxy`
    """
    
    allowed_request_methods = aslist(allowed_request_methods)
    suppress_http_headers = aslist(suppress_http_headers)
    timeout = timeout and int(timeout) or None
    return Proxy(
        address,
        timeout = timeout,
        allowed_request_methods=allowed_request_methods,
        suppress_http_headers=suppress_http_headers)

class TransparentProxy(object):
    """
    A proxy that sends the request just as it was given, including
    respecting HTTP_HOST, wsgi.url_scheme, etc.

    This is a way of translating WSGI requests directly to real HTTP
    requests.  All information goes in the environment; modify it to
    modify the way the request is made.

    If you specify ``force_host`` (and optionally ``force_scheme``)
    then HTTP_HOST won't be used to determine where to connect to;
    instead a specific host will be connected to, but the ``Host``
    header in the request will remain intact.
    
    如果找不到服务器则返回 404 状态
    
    如果 httplib2 在请求期间抛出异常将一律返回 502 状态 (502 Bad Gateway)
    """

    def __init__(self, cache = None, timeout = None, force_host=None,
                 force_scheme='http'):
        self.force_host = force_host
        self.force_scheme = force_scheme
        self.http = httplib2.Http(cache = cache, timeout = timeout)
        # 502 Bad Gateway
        # The server, while acting as a gateway or proxy, 
        # received an invalid response from the upstream server it accessed in attempting to fulfill the request. 
        self._bad_gateway_app = HTTPStatus(502)
        self._not_found_app = HTTPStatus(404)
        self._logger = logging.getLogger(self.__class__.__name__)
        
    def __repr__(self):
        return '<%s %s force_host=%r force_scheme=%r>' % (
            self.__class__.__name__,
            hex(id(self)),
            self.force_host, self.force_scheme)

    def __call__(self, environ, start_response):
        scheme = environ['wsgi.url_scheme']
        if self.force_host is None:
            conn_scheme = scheme
        else:
            conn_scheme = self.force_scheme
        if 'HTTP_HOST' not in environ:
            raise ValueError(
                "WSGI environ must contain an HTTP_HOST key")
        host = environ['HTTP_HOST']
        if self.force_host is None:
            conn_host = host
        else:
            conn_host = self.force_host
        headers = {}
        for key, value in environ.items():
            if key.startswith('HTTP_'):
                key = key[5:].lower().replace('_', '-')
                headers[key] = value
        # headers['host'] = host
        if 'host' in headers:
            del headers["host"]
        if 'REMOTE_ADDR' in environ and 'HTTP_X_FORWARDED_FOR' not in environ:
            headers['x-forwarded-for'] = environ['REMOTE_ADDR']
        if environ.get('CONTENT_TYPE'):
            headers['content-type'] = environ['CONTENT_TYPE']
        if environ.get('CONTENT_LENGTH'):
            length = int(environ['CONTENT_LENGTH'])
            body = environ['wsgi.input'].read(length)
            if length == -1:
                environ['CONTENT_LENGTH'] = str(len(body))
        elif 'CONTENT_LENGTH' not in environ:
            body = ''
            length = 0
        else:
            body = ''
            length = 0
        path = (environ.get('SCRIPT_NAME', '') + environ.get('PATH_INFO', ''))
        path = urllib.quote(path)
        path = conn_scheme + "://" + conn_host + path
        if 'QUERY_STRING' in environ:
            path += '?' + environ['QUERY_STRING']
        try:
            res, res_body = self.http.request(path, environ['REQUEST_METHOD'], body, headers)
        except httplib2.ServerNotFoundError:
            return self._not_found_app(environ, start_response)
        except:
            self._logger.error("proxy request fail.", exc_info = True)
            return self._bad_gateway_app(environ, start_response)
        headers_out = filter_res_headers(res)
        status = '%s %s' % (res.status, res.reason)
        start_response(status, headers_out)
        return [res_body]

def make_transparent_proxy_app(global_conf, timeout = None, force_host=None, force_scheme='http'):
    """
    Create a proxy that connects to a specific host, but does
    absolutely no other filtering, including the Host header.
    
    paste EGG Entry Point::
        
        transparent_proxy
        
    用 PasteDeploy 部署::
        
        [app:transparent_proxy]
        use = egg:khan#transparent_proxy
        timeout = 10
        
    .. seealso::
        
        :class:`TransparentProxy`
    """
    
    timeout = timeout and int(timeout) or None
    return TransparentProxy(timeout = timeout, force_host=force_host, force_scheme=force_scheme)
