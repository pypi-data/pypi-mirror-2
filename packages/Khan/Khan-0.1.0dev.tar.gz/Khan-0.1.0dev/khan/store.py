# -*- coding: utf-8 -*-

"""
简单存储支持
=================================

本模块提供工具去储存简单数据.

索引
=================================

* :func:`get_backend`
* :class:`INIStore`
* :class:`RPCStore`
* :class:`ExpireStore`
* :class:`CacheStore`
* :class:`RPCStoreService`

=================================

.. autofunction:: get_backend
.. autoclass:: INIStore
.. autoclass:: RPCStore
.. autoclass:: ExpireStore
.. autoclass:: CacheStore
.. autoclass:: RPCStoreService
"""

import time, random, os
from UserDict import DictMixin
from configobj import ConfigObj
from shove import BaseStore, Shove, getbackend, stores, caches
from shove.store.dbm import DbmStore
from khan.json import JSONRPCService, JSONRPCClient
from khan.utils.functional import synchronized
from khan.deploy import loadobject

__all__ = ["CacheStore", "RPCStoreService", "INIStore", "RPCStore", "ExpireStore", "get_backend"]

class ShoveBaseStore(BaseStore):
    
    def has_key(self, key):
        return self.__contains__(key)
     
class CacheStore(Shove):
    """
    ``Shove`` 类的封装
    
    .. seealso::
        
        ``Shove`` <http://pypi.python.org/pypi/shove>_
    """
     
    @staticmethod
    def create(store_uri = None, cache_uri = None, **kw):
        """ 
        建立一个 :class:`CacheStore` 对象
        
        :param store_uri: ``Shove`` 存储插件的 uri
        :param cache_uri: ``Shove`` 缓存插件的 uri
        :param kw: 传递给存储和缓存插件类的额外初始化参数
        
        :type store_uri: string
        :type store_uri: string
        :type kw: dict
        
        :rtype: :class:`CacheStore`
        """
        
        # Load store
        store = getbackend(store_uri or "simple://", stores, **kw)
        # Load cache
        cache = getbackend(cache_uri or "simple://", caches, **kw)
        return CacheStore(store, cache, int(kw.get("sync", 2)))
    
    def __init__(self, store, cache, sync = 2):
        """
        :param store: 一个实现了 dict 接口的存储介质
        :param cache: 一个实现了 dict 接口的存储介质
        """
        
        self._store = store
        self._cache = cache
        # Buffer for lazy writing and setting for syncing frequency
        self._buffer, self._sync = dict(), sync
        
    def __contains__(self, key):
        return key in self._cache or key in self._store
    
def get_backend(uri, **options):
    """
    根据 uri 取得一个 ``Shove`` 存储插件
    
    :param uri: ``Shove`` 存储插件的 uri
    :param options: 传递给存储和缓存插件类的额外初始化参数
    
    :rtype: ``Shove.BaseStore``
    """
    
    return getbackend(uri, stores, **options)

class KhanDBMStore(DbmStore):
    """
    改进的 dbm store， 因为在一些系统下 dbm 低层操作的 bsddb py 库不支持 unicode 作为 key

    .. warn::

        self.keys() 函数返回 unicode 的列表
    """
    
    init = "khan.dbm://"

    def _uni_to_base(self, key):
        return key.encode("utf-8", "ignore") if isinstance(key, unicode) else key

    def __setitem__(self, key, value):
        return super(KhanDBMStore, self).__setitem__(self._uni_to_base(key), value)

    def __getitem__(self, key):
        return super(KhanDBMStore, self).__getitem__(self._uni_to_base(key))

    def __delitem__(self, key):
        super(KhanDBMStore, self).__delitem__(self._uni_to_base(key))

    def __contains__(self, item):
        return super(KhanDBMStore, self).__contains__(self._uni_to_base(item))

    def keys(self):
        # FIXME 返回类型处理
        return [key.decode('utf-8', 'ignore') for key in super(KhanDBMStore, self).keys()]

class ExpireStore(DictMixin): 
    """
    本类封装一个实现了 dict 接口的存储介质，使得通过本类访问该存储介质的元素可有时间限制, 
    即： 如果一个元素在规定时间内没有被访问则会自动过期
    
    示例::
        
        store = ExpireStore(get_backend("dbm:///abc.db"))
        store = ExpireStore(Shove("dbm:///abc.db"))
    """
    
    def __init__(self, store, expires = None, max_entries = None, maxcull = None):
        """
        :param store: 一个实现了 dict 接口的存储介质, 不能是 :class:`ExpireStore` 自身
        :param expires: 元素过期时间(秒)，默认为 600 （10 分钟)
        :param max_entries: 容器内元素的最大数量, 默认为不限制, 如果设置了该值，那么当元素数量超过限制的时候，
            将随机删除其中的 ``maxcull`` 个元素
        :param maxcull: 和 ``max_entries`` 参数配合使用, 默认为 50
        """
        
        assert not isinstance(store, ExpireStore), ValueError("`store`  invalid")
        # Get random seed
        random.seed()
        # Set max entries
        self._max_entries = max_entries and int(max_entries)
        # Set maximum number of items to cull if over max
        self._maxcull = maxcull and int(maxcull) or 50
        # Set timeout
        self._expires = expires and int(expires) or 600
        self._store = store
    
    def __repr__(self):
        return repr(self._store)
    
    def __getitem__(self, key):
        try:
            exp, value = self._store[key]
        except TypeError:
            # 值不是一个 tuple(exp, value)
            del self._store[key]
            raise KeyError('%s' % key)
        else:
            cur_time = time.time()
            # Delete if item timed out.
            if exp < cur_time:
                del self._store[key]
                raise KeyError('%s' % key)
            new_exp = cur_time + self._expires
            self._store[key] = (new_exp, value) 
            return value

    def __setitem__(self, key, value):
        if self._max_entries:
            # Cull values if over max # of entries
            if len(self) >= self._max_entries: 
                for key in self._store.keys():
                    exp, value = self._store[key] 
                    # Delete if item timed out.
                    if exp < time.time():
                        del self._store[key]
                if len(self) >= self._max_entries: 
                    self._cull()
        # Set expiration time and value
        exp = time.time() + self._expires
        self._store[key] = (exp, value) 
        
    def __delitem__(self, key):
        try:
            del self._store[key]
        except:
            raise KeyError('%s' % key)

    def __len__(self):
        return len(self._store)
    
    def _cull(self):
        '''Remove items in store to make room.'''
          
        num, maxcull = 0, self._maxcull
        # Cull number of items allowed (set by self._maxcull)
        for key in self.keys():
            # Remove only maximum # of items allowed by maxcull
            if num <= maxcull:
                # Remove items if expired
                try:
                    self[key]
                except KeyError:
                    num += 1
            else: break
        # Remove any additional items up to max # of items allowed by maxcull
        while len(self) >= self._max_entries and num <= maxcull:
            # Cull remainder of allowed quota at random
            del self[random.choice(self.keys())]
            num += 1            
    
    def keys(self):
        keys = []
        for key in self._store.keys():
            exp, value = self._store[key] 
            # Delete if item timed out.
            if exp < time.time():
                del self._store[key]
            else:
                keys.append(key)
        return keys
            
class RPCStoreService(JSONRPCService):
    """
    jsonrpc 服务， 和 :class:`RPCStore` 配合使用, 本类封装一个实现了 dict 接口的 store, 
    并对外提供以下几个方法以便访问该 store::
        
        store.get(key)
        store.set(key, value)
        store.remove(key)
        store.clear()
        store.len()
        store.has_key(key)
        store.keys()
    
    .. note::
        
        该 store 内只能存储简单数据(可序列化为 json 格式的数据)
    """
    
    def __init__(self, store):
        JSONRPCService.__init__(self)
        self._store = store
        self["store.get"] = self.get
        self["store.set"] = self.set
        self["store.remove"] = self.remove
        self["store.clear"] = self._store.clear
        self["store.len"] = self._store.__len__
        self["store.has_key"] = self.has_key
        self["store.keys"] = self._store.keys
    
    def __repr__(self):
        return repr(self._store)
    
    def get(self, key):
        if isinstance(key, unicode):
            key = key.encode("utf-8")
        return self._store[key]
    
    def set(self, key, value):
        if isinstance(key, unicode):
            key = key.encode("utf-8")
        self._store[key] = value
    
    def remove(self, key):
        if isinstance(key, unicode):
            key = key.encode("utf-8")
        del self._store[key]
    
    def has_key(self, key):
        if isinstance(key, unicode):
            key = key.encode("utf-8")
        return key in self._store
    
def make_rpcstore_app(global_conf, store, conf = None):
    """
    paste EGG Entry Point::
        
        rpcstore
        
    用 PasteDeploy 部署::
        
        [app:store]
        use = egg:khan#rpcstore
        store = khan.ini:///path/to/your_inifile.ini
    """
    
    conf = conf or global_conf["__file__"]
    if "://" in store:
        store = get_backend(store)
    else:
        store = loadobject("config:%s" % conf, store, global_conf)
    app = RPCStoreService(store)
    return app

def format_cache_options(options):
    if "timeout" in options:
        options["timeout"] = int(options["timeout"])
    if "max_entries" in options:
        options["max_entries"] = int(options["max_entries"])
    if "cull" in options:
        options["cull"] = int(options["cull"])
    return options

class RPCStore(ShoveBaseStore):
    """
    ``Shove`` 存储插件, 用于配合 :class:`RPCStoreService` 一起使用
    
    独立使用示例::
    
        # RPCStoreService app 的 url
        service_url = "http://localhost:7040"
        
        store = RPCStore(service_url)
    
    作为 ``Shove`` 的存储插件示例::
    
        store = Shove("khan.rpc://localhost:7040", rpc_timeout = 30, rpc_http_schema = "https")
    
    .. seealso::
        
        :class:`RPCStoreService`
    """
    
    DRIVER_NAME = "khan.rpc"
    
    def __init__(self, uri, **kw):
        """
        :param uri: `RPCStoreService`'s uri
        :param rpc_timeout: socket level timeout, default is 30 seconds.
        :param rpc_http_schema: http schema, default is `http`.
        """
        
        super(RPCStore, self).__init__(uri, **kw)
        rpc_timeout = int(kw.get('rpc_timeout', 30))
        if uri.startswith("http://") or uri.startswith("https://"):
            self._rpcclient = JSONRPCClient(uri, timeout = rpc_timeout)
        elif uri.startswith("%s://" % self.DRIVER_NAME): 
            uri = uri.split("://")[1]
            rpc_http_schema = kw.get("rpc_http_schema", "http")
            self._rpcclient = JSONRPCClient(rpc_http_schema + "://" + uri, timeout = rpc_timeout)
        else:
            raise ValueError("`uri` invalid.")
        self._updated = True
        self._keys = []
        
    def __getitem__(self, key):
        try:
            value = self._rpcclient.store.get(key)
        except:
            raise KeyError("%s" % key)
        else:
            if isinstance(value, unicode):
                value = value.encode("utf-8")
            return value
        
    def __setitem__(self, key, value):
        try:
            self._rpcclient.store.set(key, self.dumps(value))
            self._updated = True
        except:
            pass

    def __delitem__(self, key):
        try:
            self._rpcclient.store.remove(key)
            self._updated = True
        except:
            pass
    
    def __contains__(self, key):
        try:
            return self._rpcclient.store.has_key(key)
        except:
            return False 
    
    def keys(self):
        if self._updated or not self._keys:
            try:
                self._keys = self._rpcclient.store.keys()
            except:
                pass
        return self._keys
    
    def clear(self):
        try:
            self._rpcclient.store.clear()
        except:
            pass
        
class INIStore(ShoveBaseStore):
    """
    用 ini 文件作为存储介质，可读可写
    
    无 section 的 ini 文件对应的 store 结构::
        
        file.ini 文件:
        
            option = value
            option1 = value
            
        对应的 store 即为:
            
            {"option" : "value", "option1" : "value1"}
    
    有一个或者多层 section 的 ini 文件对应的 store 结构::
        
        file.ini 文件:
        
            [section1]
            option = value
            option1 = value
            
            [section2]
            option = value
            option1 = value
            
            [[section2_1]]
            option = value
            option1 = value
        
        对应的 store 即为:
        
            {'section1': {'option': 'value', 'option1': 'value'}, 
                'section2': {'option': 'value', 'option1': 'value', 'section2_1': {'option': 'value', 'option1': 'value'}}}
            
    独立使用示例::
    
        store = INIStore("/path/to/your.ini")
        
    作为 ``Shove`` 存储插件示例::
    
        store = Shove("khan.ini:///path/to/your.ini")
    """
    
    DRIVER_NAME = "khan.ini"
    
    def __init__(self, uri, parent=None, **kw):
        
        super(INIStore, self).__init__(uri, **kw)

        # 判断是否为parent
        if parent is None:
            if isinstance(uri, basestring):
                if uri.startswith("%s://" % self.DRIVER_NAME): 
                    filename = uri.split("://")[1]
                else:
                    filename = uri
                filename = os.path.abspath(filename)
                self._cp = ConfigObj(filename)
            elif hasattr(uri, "read"):
                # uri is file like object
                self._cp = ConfigObj(uri)
            else:
                raise ValueError("`uri` invalid.")
        else:
            self._cp = {}

        # 父对象
        self.parent = parent
        self.uri = uri
        
    @synchronized
    def __save__(self):
        if self.parent:
            self.parent.__save__()
        else:
            self._cp.write()
        
    def __repr__(self):
        return repr(self._cp)
    
    @synchronized
    def __getitem__(self, key):
        obj = self._cp[key]

        # 判断得到的类型
        if isinstance(obj, (
            dict, list, set, tuple)):
            _obj = INIStore(self.uri, parent = self)
            _obj._cp = obj
            obj = _obj

        return obj
    
    @synchronized
    def __setitem__(self, key, value):
        self._cp[key] = value
        self.__save__()
        
    @synchronized
    def __delitem__(self, key):
        del self._cp[key]
        self.__save__()
        
    @synchronized
    def keys(self):
        return self._cp.keys()

def make_store_object(global_conf, uri = None, cache = None, **options):
    """
    [object:store]
    use = egg:khan#store
    uri = dbm:///home/alec/a.dbm
    cache = memory://
    max_entries = 300
    """
    
    uri = uri or "memory://"
    options = format_cache_options(options)
    if cache:
        store = CacheStore.create(uri, cache, **options)
    else:
        store = get_backend(uri, **options)
    return store
