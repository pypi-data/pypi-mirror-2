# -*- coding: utf-8 -*-

"""
修饰器工具
=================================

索引
=================================

* :func:`asdecorator`
* :class:`WSGIDecoratorForClass`
* :class:`InvalidException`
* :class:`InvalidResponseFilter`
* :class:`InvalidHandler`
* :class:`HTTPStatusOnInvalid`
* :class:`RedirectOnInvalid`
* :class:`RedirectFilter`

=================================

.. autofunction:: asdecorator
.. autoclass:: WSGIDecoratorForClass
.. autoclass:: InvalidException
.. autoclass:: InvalidResponseFilter
.. autoclass:: InvalidHandler
.. autoclass:: HTTPStatusOnInvalid
.. autoclass:: RedirectOnInvalid
.. autoclass:: RedirectFilter
"""

import logging, functools
from abc import ABCMeta, abstractmethod
from webob.exc import status_map

__all__ = [
    "update_wrapper_for_handler",
    "HTTPStatusOnInvalid",
    "RedirectOnInvalid",
    "RedirectFilter",
    "InvalidException",
    "InvalidHandler",
    "InvalidResponseFilter",
    "asdecorator",
    "WSGIDecoratorForClass"
]

def update_wrapper_for_handler(wrapper, handler):
    """
    更新一个封装函数的签名，使其与 `handler` 一致.
    
    本函数通常用于 decorator 中， `handler` 可为 wsgi app 或者 webob handler
    """
    
    if hasattr(handler, "__call__"):
        func = functools.partial(handler).func
        # handler 对象此时为类，没有 __name__ 属性，所以要在 update_wrapper 时候指定不拷贝 __name__ 
        return functools.update_wrapper(wrapper, func, ("__module__", "__doc__"))
    else:
        return functools.update_wrapper(wrapper, handler)
    
def asdecorator(cls, *args, **kargs):
    """
    Example::
    
        class MyMiddleware(object):
            
            def __init__(self, app, arg1, arg2):
                pass 
        
        @asdecorator(MyMiddleware, arg1, arg2)
        def app(environ, start_response):
            pass
    """
    
    def decorator(handler):
        def wrapper(*handler_args, **handler_kargs):
            new_args = list(handler_args)
            new_args.extend(handler_kargs.values())
            # 如果 handler 将传入三个参数，那么认为该 handler 是一个类方法，
            # 因为 webob handler 只有一个参数，wsgi app 也只有两个参数
            if len(new_args) == 3:
                self = new_args[0]
                # 去掉 `self` 参数
                new_args = new_args[1 : ]
                handler_wrapper = lambda *a, **k: handler(self, *a, **k)
            else:
                handler_wrapper = handler
            return cls(handler_wrapper, *args, **kargs)(*new_args, **handler_kargs)
        return update_wrapper_for_handler(wrapper, handler)
    return decorator

class WSGIDecoratorForClass(object):
    """
    允许将用于 webob handler 或 wsgi app 的 decorator 直接用来修饰 wsgi app class

    类修饰器
    
    @WSGIDecoratedForClass(mydecorator())
    class MyApp(object):
    
        def __call__(self, environ, start_resopnse):
            pass
    """
    
    def __init__(self, decorator):
        """
        :param decorator: 用于 webob handler 或 wsgi app 的 decorator
        """
        
        self.decorator = decorator
    
    def __call__(self, cls):
        orig_call = cls.__call__
        def repl_call(controller, *args, **kargs):
            def wrapper(*args, **kargs):
                return orig_call(controller, *args, **kargs)
            return self.decorator(wrapper)(*args, **kargs)
        cls.__call__ = repl_call
        return cls
    
class InvalidException(Exception): 
    
    def __init__(self, data):
        if isinstance(data, BaseException):
            self.exception = data
            msg = data 
        elif isinstance(data, basestring):
            self.exception = Exception(data)
            msg = data
        else:
            raise TypeError("`data` invalid")
        super(InvalidException, self).__init__(msg)
        
class InvalidResponseFilter(object):
    """
    专门用于过滤 :class:`InvalidHandler` 产生的 response, 子类必须实现 :func:`__call__` 方法
    """
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def __call__(self, resp, invalid):
        """
        过滤 response, 并返回一个新的 response
        
        :param resp: ``webob.Response``
        :param invalid: :class:`khan.schema.Invalid`
        """
        
        raise NotImplementedError

class InvalidHandler(object):
    """
    本类用于当校验失败时的处理操作, 通常用于 :func:`validated` 的 ``on_invalid`` 参数
    本类支持 | 操作，即为应用 response 过滤器, 过滤器必须继承自 :class:`InvalidResponseFilter`, 
    
    例如::
        
        HTTPStatusOnInvalid(404) | FormRestorer(id="form_id") | other_filter
        
    用法示例::
        
        @FormRestorer()
        def show_form(req):
            pass
            
        @validated(MySchema, HTTPStatusOnInvalid(404) | filter | filter)
        def do_form(req):
            pass
            
    .. seealso::
        
        :class:`InvalidResponseFilter`
    """
    
    __metaclass__ = ABCMeta
    
    def __or__(self, filter):
        assert isinstance(filter, InvalidResponseFilter)
        return InvalidFilterHandler(self, [filter])
    
    @abstractmethod
    def __call__(self, req, invalid):
        raise NotImplementedError
    
class InvalidFilterHandler(object):
    
    @classmethod
    def create(cls, handler, filters):
        """
        子类如果重写了 __init__ 方法，则必须重写本方法
        
        :rtype: :class:`InvalidFilterHandler`
        """
        
        return cls(handler, filters)
    
    def __init__(self, handler, _filters = None):
        """
        :param handler: 一个可调用对象，接受一个 ``webob.Request`` 参数，并返回一个 ``webob.Response`` 实例
        """
        
        self.handler = handler
        self._filters = _filters or []
        self._logger = logging.getLogger(self.__class__.__name__)
    
    def __or__(self, filter):
        return self.__class__.create(self.handler, self._filters + [filter])
    
    def __call__(self, req, invalid):
        resp = self.handler(req, invalid)
        resp.request = req
        for filter in self._filters:
            try:
                resp = filter(resp, invalid)
            except:
                self._logger.error("filter response fail.", exc_info = True)
        return resp
        
class HTTPStatusOnInvalid(InvalidHandler):
    """
    用法示例::
        
        class ControllerA(Controller):
        
            @InspectCaller(MySchema(), HTTPStatusOnInvalid(400))
            def action(self):
                pass
            
    .. seealso::
        
        :class:`InvalidResponseFilter`
    """
    
    def __init__(self, status_int, **kargs):
        self._httpstatus = status_map[status_int](**kargs)
    
    def __call__(self, req, invalid):
        self._httpstatus.request = req
        return self._httpstatus

class RedirectOnInvalid(HTTPStatusOnInvalid):
    """
    用法示例::
        
        class ControllerA(Controller):
        
            @InspectCaller(MySchema(), RedirectOnInvalid("/other_action"))
            def action(self):
                pass
            
    .. seealso::
        
        :class:`InvalidResponseFilter`
    """
    
    def __init__(self, location, status_int = 302, **kargs):
        kargs.setdefault("location", location)
        super(RedirectOnInvalid, self).__init__(status_int, **kargs)

class RedirectFilter(InvalidResponseFilter):
    
    def __init__(self, location, status_int = 302):
        self.location = location
        self.status_int = status_int
        
    def __call__(self, resp, invalid):
        resp.location = self.location
        resp.status_int = self.status_int
        return resp