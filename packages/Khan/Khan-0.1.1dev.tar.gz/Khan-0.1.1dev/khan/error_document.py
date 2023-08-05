# -*- coding: utf-8 -*-

"""
HTTP 错误页面
=================================

本模块提供工具去处理 HTTP 错误页面.

索引
=================================

* :class:`ErrorDocument`
* :func:`make_error_document_middleware`

=================================

.. autoclass:: ErrorDocument
    :members: 
.. autofunction:: make_error_document_middleware
"""

import os, logging
import tempita
from webob import Request, Response
from webob.exc import status_map
from paste.util.converters import asbool
from khan.httpstatus import HTTPStatusDispatcher

__all__ = ["ErrorDocument"]

class ErrorDocument(object):
    """
    错误文档中间件，本中间件使用 `tempita <http://pythonpaste.org/tempita/>`_` 作为模板引擎
    
    模板文件可以使用两个变量::
        
        * request
        * status
    
    """
    
    CATCH_STATUS = [401, 403, 404, 500]
    
    FILE_EXTENSION = ".html"
    
    def __init__(self, app, document_root, catch = CATCH_STATUS,
                 keep_status = True, file_extension = FILE_EXTENSION):
        self.document_root = document_root
        self.file_extension = file_extension or self.FILE_EXTENSION
        self._not_found_app = status_map[404]()
        self._logger = logging.getLogger(self.__class__.__name__)
        self._status_dispatcher = HTTPStatusDispatcher(app, keep_status)
        for status in catch:
            self._status_dispatcher[status] = self.internal_app
        self._fcache = {}
        
    def internal_app(self, environ, start_response):
        status = environ[HTTPStatusDispatcher.ORIG_STATUS_KEY]
        headers = environ[HTTPStatusDispatcher.ORIG_HEADERS_KEY]
        status_code = status.split()[0]
        status_int = int(status_code)
        if status_int not in self._fcache:
            tpl = os.path.join(self.document_root, status_code + self.file_extension)
            if not os.path.isfile(tpl):
                self._logger.error("error document file not be found '%s'" % file)
                return status_map[status_int]()(environ, start_response)
            f = file(tpl)
            self._fcache[status_int] = tempita.HTMLTemplate(f.read())
            f.close()
        tpl = self._fcache[status_int]
        ctx = {"request" : Request(environ), "status" : status}
        try:
            
            resp = Response(tpl.substitute(ctx), content_type = "text/html", status = status)
        except:
            self._logger.error("render template fail.", exc_info = True)
            resp = status_map[status_int]()
            resp.headerlist.extend(headers)
        return resp(environ, start_response)
    
    def __call__(self, environ, start_response):
        return self._status_dispatcher(environ, start_response)
    
def make_error_document_middleware(global_conf, document_root, catch = None, 
                                   disabled = True, keep_status = True, file_extension = ErrorDocument.FILE_EXTENSION):
    """
    Paste EGG entry point::
        
        error_document
        
    PasteDeploy example::
    
        [app:main]
        use = egg:khan#status
        status = 404
        filter-with = error_document
        
        [filter:error_document]
        use = egg:khan#error_document
        disabled = %(debug)s
        document_root = %(here)s/%(package)s/templates/error_documents
        catch = 404 500
        keep_status = False
    """
    
    if asbool(disabled):
        return lambda app : app
    if catch:
        catch = map(lambda x : int(x), catch.split())
    else:
        catch = ErrorDocument.CATCH_STATUS
    def middleware(app):
        return ErrorDocument(app, document_root, catch, asbool(keep_status), file_extension)
    return middleware
