# -*- coding: utf-8 -*-

"""
InspectCaller action decorator
=================================

索引
=================================

* :class:`GETParam`
* :class:`POSTParam`
* :class:`RequestParam`
* :class:`URLParam`
* :class:`InspectCaller`

=================================

.. autoclass:: GETParam
.. autoclass:: POSTParam
.. autoclass:: RequestParam
.. autoclass:: URLParam
.. autoclass:: InspectCaller
"""

import logging, inspect
from abc import ABCMeta, abstractmethod
from webob import multidict
from khan.urlparse import urlsearch
from khan.httpstatus import HTTPStatus
from khan.utils.decorator import InvalidHandler, InvalidException
from khan import schema
from .core import ActionDecorator

__all__ = [
    "GET",
    "POST",
    "GETParam",
    "POSTParam",
    "RequestParam",
    "URLParam",
    "InspectCaller"
]

class InspectCaller(ActionDecorator):
    """
    将用户请求参数当作函数的参数来调用控制器函数(Action).
    
    示例::
        
        class MySchema(schema.Schema):
            a = String() 
            
        @InspectCaller(MySchema(), GETParam() & URLParam("/{haha}"))
        def action(self, id, haha, xx = None):
            pass
            
        @InspectCaller(MySchema(), MyHandlerOnInvalid() | RedirectFilter("/abc"), 
               POSTParam() | GETParam() | URLParam())
        def action():
            pass

        @InspectCaller(MySchema(), HTTPStatusOnInvalid(403))
        def action(self, id, haha, xx = None):
            pass
            
    .. note:: 
    
        * 如果函数签名内指定了某个参数的默认值，而 validator 也同时指定了该参数的值，那么如果客户端请求参数内没有指定该函数参数，那么该函数参数的值将是 validator 指定的值，而不是函数参数默认值。
        
        * 本 decorator 会改变被修饰函数的签名，变为::
            
            wrapper(self, *arg, **kargs)
    
    .. seealso::
        
        :class:`khan.utils.decorator.InvalidHandler`
    """
    
    def __init__(self, validator, *args, **kargs):
        """
        Constractor
        
        :param validator: :class:`khan.schema.Schema`.
        :param on_invalid: 指定参数校验无效的回调函数, 函数签名为 on_invalid(req, invalid),  
            req 为 ``webob.Request``, ``invalid`` 为 :class:`khan.schema.ValidationError` 该函数必须返回一个 ``webob.Response`` 对象，默认是 :func:`khan.utils.abort` (404).
        :param src: 请求参数来源, 默认为 :class:`RequestParam`.
        """
        
        assert isinstance(validator, schema.Schema), TypeError("`validator` invalid")
        args = kargs.values() + list(args) 
        if len(args) == 2:
            on_invalid = kargs.get("on_invalid", args[0])
            src = kargs.get("src", args[1])
        elif len(args) == 1:
            if "on_invalid" in kargs:
                on_invalid = kargs["on_invalid"]
                src = None
            elif "src" in kargs:
                src = kargs["src"]
                on_invalid = None
            else:
                arg = args[0]
                if isinstance(arg, ParamProvider):
                    src = arg
                    on_invalid = None
                elif isinstance(arg, InvalidHandler):
                    src = None
                    on_invalid = arg
                else:
                    raise ValueError("`on_invalid` or `src` arguments invalid")
        else:
            on_invalid = None
            src = None
        self.validator = validator
        self.src = src or RequestParam()
        self.on_invalid = on_invalid
        self.logger = logging.getLogger(self.__class__.__name__)
        
    def __call__(self, func):
        def wrapper(controller, *args, **kargs):
            data = multidict.MultiDict(**kargs)
            data.update(self.src(controller.request))
            # 函数参数操作
            func_args, func_varargs, func_varkw, func_defaults = inspect.getargspec(func)
            args_len = len(args)
            if args_len > 0:
                func_defaults_len = (len(func_defaults) if (not func_defaults is None) else 0)
                for i in range(1, len(func_args)):
                    func_arg_name = func_args[i]                    
                    if args_len > (i - 1):
                        data[func_arg_name] = args[i - 1]
                    else:
                        if func_defaults_len > 0:
                            defaults_pos = func_defaults_len + i
                            if func_defaults_len > defaults_pos:
                                data[func_arg_name] = func_defaults[defaults_pos]                   
            validate_result = {}
            try:
                validate_result = self.validator.convert(data)
            except schema.SchemaError, e:
                self.logger.debug("Calling '%s' method with invalid args: **%r, errors: **%r" % (
                    func.__name__, data, e))
                if self.on_invalid:
                    return self.on_invalid(controller.request, InvalidException(e))
                else:
                    return HTTPStatus(400, detail = controller.request.path_info)
            else:
                validate_result = dict(map(lambda item : (item[0].encode("utf-8"), item[1]), validate_result.items()))
                result = {}
                if func_varkw is None:
                    for k, value in validate_result.iteritems():
                        if k in func_args:
                            result[k] = value
                else:
                    result = validate_result
                self.logger.debug("Calling '%s' method with keywords args: **%r" % (func.__name__, result))
                return func(controller, **result)
        return wrapper

class ParamProvider(object):
    
    __metaclass__ = ABCMeta
    
    @abstractmethod
    def __call__(self, request):
        raise NotImplementedError
    
    def __and__(self, other):
        assert isinstance(other, ParamProvider), \
            TypeError("`other` should be a `ParamProvider` subclass")
        return AllParamProvider(self, other)

class AllParamProvider(ParamProvider):
    
    def __init__(self, *sources):
        assert sources, ValueError("`sources` invalid.")
        self.sources = sources
    
    def __call__(self, request):
        result = {}
        for s in self.sources:
            tmp_result = s(request)
            if tmp_result:
                result.update(tmp_result)
        return result
    
class GETParam(ParamProvider):
    
    def __call__(self, request):
        return request.GET

GET = GETParam()

class POSTParam(ParamProvider):
    
    def __call__(self, request):
        return request.POST

POST = POSTParam()

class RequestParam(ParamProvider):
    
    def __call__(self, request):
        return request.params

class URLParam(ParamProvider):
    
    def __init__(self, pattern):
        self.pattern = pattern
        
    def __call__(self, request):
        return urlsearch(self.pattern, request.path_info)
