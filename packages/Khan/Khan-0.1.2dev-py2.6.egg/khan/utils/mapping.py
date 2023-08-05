# -*- coding: utf-8 -*-

"""
字典工具
=================================

索引
=================================

* :func:`ismapping`
* :class:`DictDotted`
* :class:`ObjectDictify`
* :class:`DictMirror`

=================================

.. autofunction:: ismapping
.. autoclass:: DictDotted
.. autoclass:: ObjectDictify
.. autoclass:: DictMirror
"""

from UserDict import DictMixin

__all__ = ["ismapping", "DictDotted", "ObjectDictify", "DictMirror"]

def ismapping(obj):
    if isinstance(obj, dict) or (hasattr(obj, "__getitem__") and hasattr(obj, "__setitem__") and \
        hasattr(obj, "__delitem__") and hasattr(obj, "__iter__")):
        return True
    else:
        return False
    
class DictDotted(DictMixin, object):
    """
    Creates objects that behave much like a dictionaries, but allow nested
    key access using object '.' (dot) lookups.
    """
    
    def __init__(self, *args, **kargs):
        d = dict(*args, **kargs)
        for k in d:
            if ismapping(d[k]):
                self.__dict__[k] = DictDotted(d[k])
            elif isinstance(d[k], (list, tuple)):
                l = []
                for v in d[k]:
                    if ismapping(v):
                        l.append(DictDotted(v))
                    else:
                        l.append(v)
                self.__dict__[k] = l
            else:
                self.__dict__[k] = d[k]

    def __getitem__(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
    
    def __setitem__(self, name, value):
        self.__dict__[name] = value
    
    def __delitem__(self, name):
        del self.__dict__[name]
    
    def keys(self):
        return self.__dict__.keys()

class ObjectDictify(DictMixin):
    
    def __init__(self, obj, readonly = False):
        self.obj = obj
        self.readonly = readonly
        
    def __getitem__(self, key):
        if key.startswith("_"):
            raise KeyError("key `%s` invalid" % key)
        if hasattr(self.obj, key):
            return getattr(self.obj, key)
        else:
            raise KeyError(key)
        
    def __setitem__(self, key, val):
        if self.readonly:
            raise KeyError(key)
        else:
            if key.startswith("_"):
                raise KeyError("key `%s` invalid" % key)
            setattr(self.obj, key, val)
    
    def __delitem__(self, key):
        if self.readonly:
            raise KeyError(key)
        else:
            if hasattr(self.obj, key):
                delattr(self.obj, key)
            else:
                raise KeyError(key)
    
    def keys(self):
        return filter(lambda member_name : not member_name.startswith("_"), dir(self.obj))
    
class DictMirror(DictMixin):
    
    def __init__(self, data, mirrors):
        self.data = data
        if not isinstance(mirrors, (set, list, tuple)):
            mirrors = [mirrors]
        self.mirrors = mirrors
        
    def __getitem__(self, key):
        try:
            return self.data[key]
        except KeyError:
            for m in self.mirrors:
                if key in m:
                    return m[key]
        raise KeyError(key)
    
    def __setitem__(self, key, val):
        self.data[key] = val
    
    def __delitem__(self, key):
        del self.data[key]
    
    def keys(self):
        keys = []
        keys.extend(self.data.keys())
        for m in self.mirrors:
            keys.extend(m.keys())
        return set(keys)
    