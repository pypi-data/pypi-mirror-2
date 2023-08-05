# -*- coding: utf-8 -*-

"""
字典工具
=================================

索引
=================================

* :func:`assert_dict`
* :class:`PrintValue`
* :class:`DictTester`
* :class:`ProjectTester`

=================================

.. autofunction:: assert_dict
.. autoclass:: PrintValue
.. autoclass:: DictTester
.. autoclass:: ProjectTester
"""

import unittest
from unittest import TestCase, TestLoader, TextTestRunner
from nose.plugins import Plugin as NosePlugin
from webob import Response
from webtest import TestApp
from khan.utils.mapping import DictDotted
from khan.deploy import EnvironLoader

__all__ = ["unittest", "assert_dict", "DictTester", "TestCase", "TestApp", "PrintValue", "ProjectTester"]

def assert_dict(dict_like):
    class Tester(DictTester, TestCase):
        def setUp(self):
            self.store = dict_like
            super(Tester, self).setUp()
    suite = TestLoader().loadTestsFromTestCase(Tester)
    TextTestRunner(verbosity=2).run(suite)
    
class PrintValue(object):
    
    def __init__(self, value = ""):
        if not isinstance(value, basestring):
            value = repr(value)
        self.value = value
    
    def __repr__(self):
        return "<%s %s>" % (self.__class__.__name__, self.value)
    
    def __call__(self, environ, start_response):
        res = Response(self.value)
        return res(environ, start_response)

class DictTester(object):
    
    def setUp(self):
        self.store.clear()
        
    def test__getitem__(self):
        self.store['max'] = 3
        self.assertEqual(self.store['max'], 3)

        self.store.clear()
        self.store[u'最大'] = 3
        self.assertEqual(self.store[u'最大'], 3)

    def test__setitem__(self):
        self.store['max'] = 3
        self.assertEqual(self.store['max'], 3)
        
        self.store.clear()
        self.store[u'最大'] = 3
        self.assertEqual(self.store[u'最大'], 3)

    def test__delitem__(self):
        self.store['max'] = 3
        del self.store['max']
        self.assertEqual('max' in self.store, False)

        # FIXME DBM总是失败的
        self.store.clear()
        self.store[u'最大'] = 3
        del self.store[u'最大']
        self.assertEqual(u'最大' in self.store, False)
    
    def test_clear(self):
        self.store['max'] = 3
        self.store['min'] = 6
        self.store['pow'] = 7
        self.store.clear()
        self.assertEqual(len(self.store), 0)
        
        self.store.clear()
        self.store[u'最大'] = 3
        self.store[u'最小'] = 6
        self.store[u'一般'] = 7
        self.store.clear()
        self.assertEqual(len(self.store), 0)
    
    """
    def test_copy(self):
        self.store['max'] = 3
        self.store['min'] = 6
        store = self.store.copy()
        self.assertEqual(store, self.store)
        store.clear()
        self.assertNotEqual(store, self.store)
    """
    
    def test__repr__(self):
        repr(self.store)
         
    def test_get(self):
        self.store['max'] = 3
        self.assertEqual(self.store.get('max'), 3)

        self.store.clear()
        self.store[u'最大'] = 3
        self.assertEqual(self.store.get(u'最大'), 3)

    def test__len__(self):
        self.store['max'] = 3
        self.store['min'] = 6
        self.assertEqual(len(self.store), 2)

        self.store.clear()
        self.store[u'最大'] = 3
        self.store[u'最小'] = 6
        self.assertEqual(len(self.store), 2)

    def test_items(self):
        self.store['max'] = 3
        self.store['min'] = 6
        self.store['pow'] = 7
        slist = list(self.store.items())
        self.assertEqual(('min', 6) in slist, True)

        # FIXME DBM总是失败的
        self.store.clear()
        self.store[u'最大'] = 3
        self.store[u'最小'] = 6
        self.store[u'一般'] = 7
        slist = list(self.store.items())
        self.assertEqual((u'最小', 6) in slist, True)

    def test_iteritems(self):
        self.store['max'] = 3
        self.store['min'] = 6
        self.store['pow'] = 7
        slist = list(self.store.iteritems())
        self.assertEqual(('min', 6) in slist, True)

        # FIXME DBM总是失败的
        self.store.clear()
        self.store[u'最大'] = 3
        self.store[u'最小'] = 6
        self.store[u'一般'] = 7
        slist = list(self.store.iteritems())
        self.assertEqual((u'最小', 6) in slist, True)

    def test_iterkeys(self):
        self.store['max'] = 3
        self.store['min'] = 6
        self.store['pow'] = 7
        slist = list(self.store.iterkeys())
        self.assertEqual('min' in slist, True)

        # FIXME DBM总是失败的
        self.store.clear()
        self.store[u'最大'] = 3
        self.store[u'最小'] = 6
        self.store[u'一般'] = 7
        slist = list(self.store.iterkeys())
        self.assertEqual(u'最小' in slist, True)

    def test_itervalues(self):
        self.store['max'] = 3
        self.store['min'] = 6
        self.store['pow'] = 7
        slist = list(self.store.itervalues())
        self.assertEqual(6 in slist, True)
        
        self.store.clear()
        self.store[u'最大'] = 3
        self.store[u'最小'] = 6
        self.store[u'一般'] = 7
        slist = list(self.store.itervalues())
        self.assertEqual(6 in slist, True)

    def test_pop(self):
        self.store['max'] = 3
        self.store['min'] = 6
        item = self.store.pop('min')
        self.assertEqual(item, 6)
        
        self.store.clear()
        self.store[u'最大'] = 3
        self.store[u'最小'] = 6
        item = self.store.pop(u'最小')
        self.assertEqual(item, 6)
        
    def test_popitem(self):
        self.store['max'] = 3
        self.store['min'] = 6
        self.store['pow'] = 7
        item = self.store.popitem()
        self.assertEqual(len(item) + len(self.store), 4)
        
        self.store.clear()
        self.store[u'最大'] = 3
        self.store[u'最小'] = 6
        self.store[u'一般'] = 7
        item = self.store.popitem()
        self.assertEqual(len(item) + len(self.store), 4)

    def test_setdefault(self):
        self.store['max'] = 3
        self.store['min'] = 6
        self.store['pow'] = 7
        self.store.setdefault('powl', 8)
        self.assertEqual(self.store['powl'], 8)
        
        self.store.clear()
        self.store[u'最大'] = 3
        self.store[u'最小'] = 6
        self.store[u'一般'] = 7
        self.store.setdefault(u'一般其他', 8)
        self.assertEqual(self.store[u'一般其他'], 8)

    def test_update(self):
        tstore = dict()
        tstore['max'] = 3
        tstore['min'] = 6
        tstore['pow'] = 7
        self.store['max'] = 2
        self.store['min'] = 3
        self.store['pow'] = 7
        self.store.update(tstore)
        self.assertEqual(self.store['min'], 6)
        
        self.store.clear()
        tstore = dict()
        tstore[u'最大'] = 3
        tstore[u'最小'] = 6
        tstore[u'一般'] = 7
        self.store[u'最大'] = 2
        self.store[u'最小'] = 3
        self.store[u'一般'] = 7
        self.store.update(tstore)
        self.assertEqual(self.store[u'最小'], 6)

    def test_values(self):
        self.store['max'] = 3
        self.store['min'] = 6
        self.store['pow'] = 7
        slist = self.store.values()
        self.assertEqual(6 in slist, True)
        
        self.store.clear()
        self.store[u'最大'] = 3
        self.store[u'最小'] = 6
        self.store[u'一般'] = 7
        slist = self.store.values()
        self.assertEqual(6 in slist, True)

    def test_keys(self):
        self.store['max'] = 3
        self.store['min'] = 6
        self.store['pow'] = 7
        slist = self.store.keys()
        self.assertEqual('min' in slist, True)

        # FIXME DBM总是失败的
        self.store.clear()
        self.store[u'最大'] = 3
        self.store[u'最小'] = 6
        self.store[u'一般'] = 7
        slist = self.store.keys()
        self.assertEqual(u'最小' in slist, True)

class ProjectTester(TestCase):
    
    _environ = None
    
    def _environ_set(self, environ):
        self._environ = environ
    def _environ_get(self):
        if not self._environ:
            if hasattr(self, "package"):
                with EnvironLoader(self.package) as (app, deploy_context):
                    self._environ = DictDotted({"app" : app, "context" : deploy_context})
        return self._environ 
    environ = property(_environ_get, _environ_set)
    
class KhanForNose(NosePlugin):
    """
    nose 插件
    
    Test Khan base project.
    """
    
    enabled = False
    
    name = "khan"
    
    def options(self, parser, env):
        super(KhanForNose, self).options(parser, env)
        parser.add_option('--khan-server',
                          dest='khan_server',
                          metavar="NAME",
                          default=env.get('NOSE_KHAN_SERVER', "main"),
                          help=("Specifie server name in "
                                "zcml file [default: %default]"))
        parser.add_option('--khan-logging',
                          dest='khan_logging',
                          action='count',
                          default=env.get('NOSE_KHAN_LOGGING', True),
                          help=("Enable khan project logging [default: %default]"))
        parser.add_option('--khan-package',
                          dest='khan_package',
                          metavar='PACKGE',
                          default=env.get('NOSE_KHAN_PACKAGE'),
                          help="Project package.")
        parser.add_option('--khan-zcml',
                          dest='khan_zcml',
                          metavar='ZCML',
                          default=env.get('NOSE_KHAN_ZCML'),
                          help="Project zcml file.")

    def configure(self, options, conf):
        self.enabled = options.enable_plugin_khan
        package = options.khan_package
        zcml = options.khan_zcml
        logging = options.khan_logging
        server_name = options.khan_server
        self._env_loader = EnvironLoader(package, zcml, logging, server_name)
        
    def begin(self):
        print
        print "*" * 70
        print "Loading Khan project environ ..."
        print "*" * 70
        print
        self.test_app, self.deploy_context = self._env_loader.open()
    
    def beforeTest(self, test):
        if isinstance(test.test, ProjectTester):
            if hasattr(test.test, "_environ"):
                if not test.test._environ:
                    test.test._environ = DictDotted({"app" : self.test_app, "context" : self.deploy_context})
                
    def finalize(self, result):
        print
        print "*" * 70
        print "Closed Khan project environ."
        print "*" * 70
        print
        try:
            self._env_loader.close()
        except:
            pass
