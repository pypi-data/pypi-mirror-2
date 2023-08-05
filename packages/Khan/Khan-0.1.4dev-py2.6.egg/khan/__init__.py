# -*- coding: utf-8 -*-

u"""
.. data:: NAMESPACE 

    khan 的命名空间    
"""

try:
    __import__('pkg_resources').declare_namespace(__name__)
except ImportError:
    from pkgutil import extend_path
    __path__ = extend_path(__path__, __name__)

NAMESPACE = "http://bitbucket.org/khan/khan"
