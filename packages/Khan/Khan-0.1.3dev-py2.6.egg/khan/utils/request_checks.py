# -*- coding: utf-8 -*-

"""
字典工具
=================================

索引
=================================

* :func:`reqchecker`
* :class:`Has`
* :class:`Equal`
* :class:`StartsWith`
* :class:`EndsWith`

=================================

.. autofunction:: reqchecker
.. autoclass:: Has
.. autoclass:: Equal
.. autoclass:: StartsWith
.. autoclass:: EndsWith
"""

from webob import Request
from .decorator import HTTPStatusOnInvalid, update_wrapper_for_handler, InvalidException

__all__ = [
    "Has",
    "Equal",
    "StartsWith",
    "EndsWith",
    "reqchecker"
]

def convert_keys_tolower(var):
    new_var = {}
    for k, v in var.items():
        if isinstance(k, basestring):
            k = k.lower()
        new_var[k] = v
    return new_var

class EnvironChecker(object):
    
    def __or__(self, other_checker):
        return AnyEnvironChecker(self, other_checker)
    
    def __and__(self, other_checker):
        return AllEnvironChecker(self, other_checker)

    def __invert__(self):
        return NotEnvironChecker(self)
    
    def __call__(self, environ):
        raise NotImplementedError

class NotEnvironChecker(EnvironChecker):
    
    def __init__(self, checker):
        self.checker = checker
    
    def __call__(self, environ):
        return not self.checker(environ)
    
class AnyEnvironChecker(EnvironChecker):
    
    def __init__(self, *checkers):
        self.checkers = checkers
    
    def __call__(self, environ):
        # checkers is empty
        if not self.checkers:
            return False
        for checker in self.checkers:
            if checker(environ):
                return True
        return False
  
class AllEnvironChecker(EnvironChecker):
    
    def __init__(self, *checkers):
        self.checkers = checkers
    
    def __call__(self, environ):
        # checkers is empty
        if not self.checkers:
            return False
        for checker in self.checkers:
            if not checker(environ):
                return False
        return True
    
class Has(EnvironChecker):
    
    def __init__(self, *keys):
        self.keys = map(lambda x : x.lower(), keys)
    
    def __call__(self, environ): 
        # self.keys is empty
        if not self.keys:
            return False
        environ = convert_keys_tolower(environ)
        for k in self.keys:
            if k not in environ:
                return False
        return True
    
class Equal(EnvironChecker):
    
    def __init__(self, case_sensitive = False, **kargs):
        self.kargs = kargs
        self.case_sensitive = case_sensitive
    
    def __call__(self, environ):
        # self.keys is empty
        if not self.kargs:
            return False
        environ = convert_keys_tolower(environ)
        for k, v in self.kargs.items():
            if k not in environ:
                return False
            val = environ[k]
            if isinstance(val, basestring):
                if not self.case_sensitive:
                    val = val.lower()
                    v = v.lower()
            if v != val:
                return False
        return True

class StartsWith(EnvironChecker):
    
    def __init__(self, key, val):
        self.key = key
        self.val = val
        
    def __call__(self, environ):
        environ = convert_keys_tolower(environ)
        if self.key in environ:
            val = environ[self.key]
            if isinstance(val, basestring):
                return val.startswith(self.val)
        return False

class EndsWith(EnvironChecker):
    
    def __init__(self, key, val):
        self.key = key
        self.val = val
        
    def __call__(self, environ):
        environ = convert_keys_tolower(environ)
        if self.key in environ:
            val = environ[self.key]
            if isinstance(val, basestring):
                return val.endswith(self.val)
        return False
    
def reqchecker(checker, on_invalid = None):
    """
    Restricts access to the function depending on ``environ``

    Example::
            
        @reqchecker(Equal(request_method = 'GET') & Has("referrer"), HTTPStatusOnInvalid(405))
        def app(environ, start_response):
            pass
        
        # '~' 用于表示 not
        @reqchecker(~ Equal(request_method = 'GET'), HTTPStatusOnInvalid(405))
        def app(environ, start_response):
            pass
            
    :param checker: :class:`EnvironChecker`
    :param on_invalid: :class:`InvalidHandler`, 默认是 :class:`HTTPStatusOnInvalid` (400)
    """
    
    on_invalid = on_invalid or HTTPStatusOnInvalid(400)
                    
    def d(handler):
        def check(*args, **kargs):
            """Wrapper for reqchecker"""
            new_args = list(args)
            new_args.extend(kargs.values())
            # wsgi app
            if len(new_args) == 2:
                environ = new_args[0]
                is_wsgiapp = True
            # webob handler
            elif len(new_args) == 1:
                is_wsgiapp = False
                environ = new_args[0].environ
            else:
                raise ValueError("`handler` invalid")
            if not checker(environ):
                resp = on_invalid(Request(environ), InvalidException("request restricted"))
                if is_wsgiapp:
                    return resp(*args, **kargs)
                else:
                    return resp
            else:
                return handler(*args, **kargs)
        return update_wrapper_for_handler(check, handler)
    return d
