# -*- coding: utf-8 -*-

"""
控制器 WSGI App
=================================

本模块提供工具去实现常见的``控制器``.

索引
=================================

* :class:`Controller`
* :class:`ActionDecorator`
* :class:`Expose`
* :class:`WSGIDecoratorForAction`

=================================

.. autoclass:: Controller
.. autoclass:: ActionDecorator
.. autoclass:: Expose
.. autoclass:: WSGIDecoratorForAction

"""

import logging, functools
from abc import ABCMeta, abstractmethod
from webob import Response, Request
from khan.utils import AsResponse, NoDefault
from khan.httpstatus import HTTPStatus

__all__ = [
    "ActionDecorator",
    "WSGIDecoratorForAction",
    "Expose",
    "Controller"
]

def _expose_action(action):
    action._expose = True
    return action

def action_is_expose(action):
    return hasattr(action, "_expose") and action._expose

class ActionDecoratorMeta(ABCMeta):
            
    def __new__(cls, classname, bases, classdict):
        cls = ABCMeta.__new__(cls, classname, bases, classdict)
        orig__call__ = cls.__call__
        def __call__(self, action):
            if hasattr(self, "__ActionDecoratorMeta__"):
                return orig__call__(self, action)
            else:
                self.__ActionDecoratorMeta__ = True
                decorator = orig__call__(self, action)
                new_action = functools.update_wrapper(decorator, action)
                new_action = _expose_action(new_action)
                return new_action
        cls.__call__ = __call__
        return cls
    
class ActionDecorator(object):
    """ 
    action decorator 基类， 
    从本类派生的类都会自动使被修饰 action 函数公开 (控制器内不公开的 action 是不允许被调用的) 
    """
    
    __metaclass__ = ActionDecoratorMeta
    
    @abstractmethod
    def __call__(self, action):
        raise NotImplementedError

class Expose(ActionDecorator):
    """
    使一个 action 可以被调用
    
    example::
        
        @Expose()
        def action(self): 
            return Response("")
    """
    
    def __call__(self, action):
        return action
    
class WSGIDecoratorForAction(ActionDecorator):
    """
    允许将用于 webob handler 或 wsgi app 的 decorator 用在 action 上 
    
    例子::
        
        @WSGIDecoratorForAction(reqchecker(Equal(request_method = "post")))
        def action(self):
            return Response()
    """
    
    def __init__(self, decorator):
        """
        :param decorator: 用于 webob handler 或 wsgi app 的 decorator
        """
        
        self.decorator = decorator
    
    def __call__(self, action):
        action_args_data = []
        # 有些 decorator 可能需要读写 handler 函数属性，所以这里要把函数独立出来而不放在 wrapper 里面，
        # 以免每次调用都需要构建 handler 函数，导致函数的属性丢失
        def app(environ, start_response):
            controller, args, kargs = action_args_data[0]
            return action(controller, *args, **kargs)(environ, start_response)
        def wrapper(controller, *args, **kargs):
            if action_args_data:
                action_args_data.pop()
            action_args_data.append((controller, args, kargs))
            return AsResponse(self.decorator(app))
        return wrapper

def _setclassattr(self, name, kargs, default):
        if hasattr(self, name):
            setattr(self, name, kargs.pop(name, getattr(self, name)))
        else:
            self.__dict__[name] = kargs.pop(name, default) 
    
class ControllerMeta(type):
                    
    def __new__(cls, classname, bases, classdict):
        cls = type.__new__(cls, classname, bases, classdict)
        orig__init__ = cls.__init__
        def __init__(self, *args, **kargs):
            if hasattr(self, "__ControllerMeta__"):
                orig__init__(self, *args, **kargs)
            else:
                self.__ControllerMeta__ = True
                _setclassattr(self, "default", kargs, default = NoDefault)
                orig__init__(self, *args, **kargs)
        cls.__init__ = __init__
        return cls

class Controller(object):
    """
    控制器基类.
    
    控制器内基本的调用单位为 ``action``, 默认情况下，action 也就是控制器的一个实例方法，
    每个 action 都必须返回一个 ``webob.Response`` 实例.
    每个 action 必须应用了从 :class:`ActionDecorator` 派生的 ``decorator`` 才允许调用，
    然而，子类也可以通过重写本类的系列函数来改变这种行为.
    
    控制器请求执行流程:
        
    1. 首先调用 :meth:`__before__` (request) 取得 request
    2. 调用 :meth:`__action__` (request) 取得 action 名字
    3. 调用 :meth:`__resolve__` (request, action) 取得一个 **可调用** 对象
    4. 调用 **可调用** 对象并取得一个 `webob.Response` 对象返回给客户端
    
    .. attribute:: logger, request
    
    ::TODO:: 
        
        要有种机制可以让子类合理地终止请求执行流程，例如给所有 action 加上身份验证
    """
    
    __metaclass__ = ControllerMeta
    
    DEFAULT_ACTION = "index"
    
    _request = None
    
    @property
    def logger(self):
        if not hasattr(self, "_logger"):
            self._logger = logging.getLogger(self.__class__.__name__)
        return self._logger
    
    @property
    def request(self):
        return self._request
    
    def __action__(self, request):
        """
        从 `webob.Request` 对象内取得 action 名，返回值为字符串，
        取得的 action 名将会传递给 :meth:`__resolve__` 进一步取得 action 对象
        
        默认实现是把 url 第一段作为 action 名字， 例如 url '/a/b/c'， 'a' 就是 action 名 
        """
        
        path_info = request.path_info.strip()
        if not path_info.startswith("/"):
            path_info = "/" + path_info
        if path_info == "/":
            return 
        if path_info.endswith("/"):
            path_info = path_info[0 : -1]
        path_spec = path_info.split("/")
        if len(path_spec) > 1:
            return path_spec[1]
        
    def __before__(self, req):
        return req
    
    def __after__(self, resp):
        return resp
    
    def __resolve__(self, request, action):
        """
        本方法必须返回一个 **可调用** 对象, 该对象签名为 `callback(controller)`，
        并且必须返回一个 `webob.Response` 对象
        """
        
        action = action.replace("-", "_")
        if action.startswith("_"):
            if hasattr(self, action):
                self.logger.debug("action '%s' starts with _, private action not allowed. " 
                          "Returning a 404 response" % action)
            return
        if isinstance(action, unicode):
            try:
                action = action.encode("utf-8")
            except:
                self.logger.debug("action '%s' can't encode with utf-8. "
                        "Returning a 404 response" % action)
                return
        if not hasattr(self, action):
            self.logger.debug("action '%s' not exists. "
                        "Returning a 404 response" % action)
            return
        action_method = getattr(self, action)
        # FIXME: 如果子类重写本函数则可绕过 action 导出的约定？
        if not action_is_expose(action_method):
            self.logger.debug("Action %r is not exposed" % action_method)
            return
        return lambda controller : action_method()
    
    def __call__(self, *args, **kargs):
        new_args = list(args)
        new_args.extend(kargs.values())
        new_args_len = len(new_args)
        # webob caller
        if new_args_len == 1:
            request = new_args[0]
        # wsgi caller
        elif new_args_len == 2:
            request = Request(new_args[0])
        else:
            raise ValueError("arguments invalid.")
        self._request = self.__before__(request)
        action = self.__action__(self._request)
        if not action:
            if self.default is NoDefault:
                action = self.DEFAULT_ACTION
            else:
                action = self.default
        resp = None
        cb = self.__resolve__(self._request, action)
        if not cb:
            self.logger.debug("action '%s' invalid. "
                        "Returning a 404 response" % action)
            resp = HTTPStatus(404)
        else:
            if not resp:
                resp = cb(self)
                if not isinstance(resp, Response):
                    self.logger.error("""action '%s' returned a invalid value that should be a `webob.Response` object.""" 
                                      % action)
                    resp = HTTPStatus(500)
        resp.request = self._request
        if new_args_len == 2:
            return self.__after__(resp)(*args, **kargs)
        else:
            return self.__after__(resp)
