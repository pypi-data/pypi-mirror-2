# -*- coding: utf-8 -*-

"""
压缩与文件最优化支持
=================================

索引
=================================

* :class:`WebMinifierPlugin`
* :class:`WebMinifier`
* :func:`make_webminifier_middleware`

=================================

.. autoclass:: WebMinifierPlugin
.. autoclass:: WebMinifier
.. autofunction:: make_webminifier_middleware
"""

import logging
from abc import ABCMeta, abstractmethod, abstractproperty
import slimmer
from webob import Response

__all__ = ["WebMinifierPlugin", "WebMinifier"]

class WebMinifierPluginMeta(ABCMeta):

    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, "_sub_classes"):
            cls._sub_classes = []
        else:
            cls._sub_classes.append(cls)

class WebMinifierPlugin(object):
    
    __metaclass__ = WebMinifierPluginMeta
    
    @abstractproperty
    def mimetypes(self):
        raise NotImplementedError

    @abstractmethod
    def __call__(self, resp):
        raise NotImplementedError

class SlimmerForWebMinifier(WebMinifierPlugin):
    
    mimetypes = ['application/x-javascript', "text/javascript", "application/javascript", "text/ecmascript", \
                 'text/css', 'text/html', 'text/xhtml', 'text/xml']
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def __call__(self, resp):
        content_type = resp.content_type.lower()
        slimmer_method = None
        if content_type in ['application/x-javascript', "text/javascript", "application/javascript", "text/ecmascript"]:
            slimmer_method = slimmer.js_slimmer
        elif content_type == 'text/css':
            slimmer_method = slimmer.css_slimmer
        elif content_type in ['text/html', 'text/xhtml', 'text/xml']:
            slimmer_method = slimmer.html_slimmer
        else:
            self.logger.debug("Content-Type of the response not in %r" % self.mimetypes)
            return resp
        # 如果出错，直接返回
        try:
            resp.body = slimmer_method(resp.body)
        except:
            self.logger.error("Can't minifies response", exc_info = True)
        return resp
        
class WebMinifier(object):
    '''
    文本最小化中间件, 支持 css/js/html/xml 等
    '''

    def __init__(self, app, catch_status = None):
        self.app = app
        self.catch_status = catch_status or [200]
        self.logger = logging.getLogger(self.__class__.__name__)
        self.plugins = map(lambda cls : cls(), WebMinifierPlugin._sub_classes)
        
    def __call__(self, environ, start_response):
        orig_response = []
        def repl_start_response(status, headers, exc_info=None):
            orig_response[ : ] = status, headers
            lambda x : None
        app_iter = self.app(environ, repl_start_response)
        if not orig_response:
            raise Exception("The app %r has not been called `start_response()`" % self.app)
        resp = Response(app_iter = app_iter, status = orig_response[0], headers = orig_response[1])
        if resp.status_int not in self.catch_status:
            return resp(environ, start_response)
        content_type = resp.content_type.lower()
        for plugin in self.plugins:
            if content_type in plugin.mimetypes:
                resp = plugin(resp)
                break
        return resp(environ, start_response)
             
def make_webminifier_middleware(global_conf, catch_status = None):
    """
    Paste EGG entry point::
        
        minifier
        
    PasteDeploy example::
        
        [app:static]
        use = egg:khan#static
        filter-with = minifier
        
        [filter:minifier]
        use = egg:khan#minifier
    """
    
    def filter(app):
        if catch_status:
            catch_status = map(lambda i : int(i), catch_status.split())
        return WebMinifier(app, catch_status = catch_status)
    return filter
