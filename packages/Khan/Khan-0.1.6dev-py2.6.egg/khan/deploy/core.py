# -*- coding: utf-8 -*-

from __future__ import absolute_import
import os, sys, logging, pkg_resources, re
from enum import Enum
from UserDict import UserDict
from zope.configuration.config import ConfigurationMachine
from zope.configuration import xmlconfig
from zope.configuration.exceptions import ConfigurationError
from zope.component import provideUtility
from zope.interface import implements
from paste.deploy.loadwsgi import _ObjectType, loadobj, fix_call, \
    loadapp as _loadapp, loadfilter as _loadfilter, loadserver as _loadserver
from paste.fixture import TestApp
from paste.registry import restorer
from khan.deploy.zcml import IAppFactory, IMiddlewareFactory, ICompositeFactory, IObjectFactory, \
     IServerFactory, ILoggingObject, IDefaultVarFactory

__all__ = ["loadobject", "loadapp", "loadfilter", "loadserver",
           "run_server_from_zcml", "make_app_from_zcml", "EnvironLoadable", "EnvironLoader"]

objectTypes = Enum("SERVER", "APP", "FILTER", "OBJECT")

def make_filter_from_mfactory(deploy_ctx, name):
    mfactory = deploy_ctx["filter_factory"]
    global_conf = deploy_ctx["global_conf"]
    if name not in mfactory:
        return
    mattrs = mfactory[name]
    muse, mparams, mnext = mattrs["use"], mattrs["params"], mattrs["next"]
    # 确保 next 属性不指向自己
    if mnext and mnext == name:
        raise ConfigurationError("'next' attribute %r of filter(%r) invalid." % (mnext, name))

    mglobal_conf = {}
    mglobal_conf.update(global_conf)
    mglobal_conf["loader"] = Loader(deploy_ctx, name)
    if isinstance(muse, basestring):
        filter = loadfilter(muse, global_conf = mglobal_conf, **mparams)
        if filter is None:
            raise ConfigurationError("load filter %r failure." % muse)
    else:
        filter = muse(mglobal_conf, **mparams)
    return filter

def make_app_from_afactory(deploy_ctx, name):
    afactory = deploy_ctx["app_factory"]
    global_conf = deploy_ctx["global_conf"]
    if name not in afactory:
        return
    app_use, app_params, _ = afactory[name]["use"], \
        afactory[name]["params"], afactory[name]["filter"]
    app_global_conf = {}
    app_global_conf.update(global_conf)
    app_global_conf["loader"] = Loader(deploy_ctx, name)
    if isinstance(app_use, basestring):
        app = loadapp(app_use, global_conf = app_global_conf, **app_params)
        if app is None:
            raise ConfigurationError("load app %r failure." % app_use)
    else:
        app = app_use(app_global_conf, **app_params)
    return app

def make_app_from_cfactory(deploy_ctx, name):
    cfactory = deploy_ctx["composite_factory"]
    global_conf = deploy_ctx["global_conf"]
    if name not in cfactory:
        return
    app_use, app_params, app_filter = cfactory[name]["use"], \
        cfactory[name]["params"], cfactory[name]["filter"]
    app_global_conf = {}
    app_global_conf.update(global_conf)
    loader = Loader(deploy_ctx, name)
    app_global_conf["loader"] = loader
    if isinstance(app_use, basestring):
        app = loadapp(app_use, global_conf = app_global_conf, **app_params)
        if app is None:
            raise ConfigurationError("load app %r failure." % app_use)
    else:
        app = app_use(loader, app_global_conf, **app_params)
    return app

def make_app_from_zcml(package = None, zcml = None, server_name = "main"):
    deploy_ctx = get_context_from_zcml(package, zcml)
    wsgiapp = make_app_from_server(deploy_ctx, server_name)
    return wsgiapp

def make_app_from_server(deploy_ctx, server_name):
    sfactory = deploy_ctx["server_factory"]
    if server_name not in sfactory:
        return
    _server = sfactory[server_name]
    server_config = _server['config']
    app = None
    if 'app' in server_config:
        # 得到主APP
        app_name = server_config.pop('app').strip()
        app = get_app(deploy_ctx, app_name)
        if app is None:
            raise ConfigurationError("app `%s` not be found or invalid" % app_name)
    elif 'pipeline' in server_config:
        pipeline = server_config.pop('pipeline').strip()
        if not pipeline:
            raise ConfigurationError("`pipeline` invalid")
        middleware_names = pipeline[1 : -1]
        # TODO:: 是否把 pipeline 中指定了 next 属性的 middleware 过滤掉或者报错？
        middleware_names.reverse()
        for mname in middleware_names:
            filter = make_filter_from_mfactory(deploy_ctx, mname)
            if filter is None:
                raise ConfigurationError("filter `%s` not be found or invalid" % mname)
            app = filter(app)
    return app

def make_server_from_sfactory(deploy_ctx, server_name):
    sfactory = deploy_ctx["server_factory"]
    global_conf = deploy_ctx["global_conf"]
    if server_name not in sfactory:
        return
    _server = sfactory[server_name]
    server_entry_point = _server['entry_point']
    server_params = _server['params']
    app = make_app_from_server(deploy_ctx, server_name)
    if app is None:
        raise ConfigurationError("No valid app related with server(name='%s')" % server_name)
    # 分开处理使用use属性
    if isinstance(server_entry_point, basestring):
        server_runner_obj = get_object_from_uri(global_conf, server_entry_point, obj_type = objectTypes.SERVER,
                                                       ** server_params)
        if server_runner_obj is None:
            raise ConfigurationError("server `%s` not be found or invalid" % server_name)
        server_runner = lambda : server_runner_obj(app)
    else:
        server_runner = lambda : server_entry_point(app, global_conf, ** server_params)
    return server_runner

def make_object_from_ofactory(deploy_ctx, name):
    ofactory = deploy_ctx["object_factory"]
    global_conf = deploy_ctx["global_conf"]
    if name not in ofactory:
        return
    oglobal_conf = {}
    oglobal_conf.update(global_conf)
    oglobal_conf["loader"] = Loader(deploy_ctx, name)
    ouse = ofactory[name]["use"]
    if isinstance(ouse, basestring):
        return loadobject(ouse, global_conf = oglobal_conf, ** ofactory[name]["params"])
    else:
        return ouse(oglobal_conf, ** ofactory[name]["params"])

def get_app_from_mfactory(deploy_ctx, name):
    mfactory = deploy_ctx["filter_factory"]
    for mname, mattrs in mfactory.items():
        muse, mparams, mnext = mattrs["use"], mattrs["params"], mattrs["next"]
        if mname == name:
            if not mnext:
                return
            app = get_app(deploy_ctx, mnext)
            if app is not None:
                filter = make_filter_from_mfactory(deploy_ctx, mname)
                if not filter:
                    raise ConfigurationError("load filter %r failure." % muse)
                return filter(app)
            else:
                raise ConfigurationError("app or filter %r not be found." % mnext)

def get_app_from_afactory(deploy_ctx, name):
    mfactory = deploy_ctx["filter_factory"]
    afactory = deploy_ctx["app_factory"]
    if name not in afactory:
        return
    app_use, app_params, app_filter = afactory[name]["use"], \
        afactory[name]["params"], afactory[name]["filter"]
    if app_filter:
        for mname, mattrs in mfactory.items():
            muse, mparams, mnext = mattrs["use"], mattrs["params"], mattrs["next"]
            if app_filter == mname :
                if mnext and mnext != name:
                    # 配置冲突，middleware 的 next 属性指定的 app, 该 app 的 filter 属性又指定了另外的 middleware
                    raise ConfigurationError("'next' attribute %r invalid." % mnext)
                app = make_app_from_afactory(deploy_ctx, name)
                filter = make_filter_from_mfactory(deploy_ctx, mname)
                if app is None:
                    raise ConfigurationError("load app %r failure." % name)
                if filter is None:
                    raise ConfigurationError("load filter %r failure." % mname)
                return filter(app)
    else:
        app = make_app_from_afactory(deploy_ctx, name)
        if app is None:
            raise ConfigurationError("load app %r failure." % name)
        return app

def get_app_from_cfactory(deploy_ctx, name):
    mfactory = deploy_ctx["filter_factory"]
    cfactory = deploy_ctx["composite_factory"]
    if name not in cfactory:
        return
    app_use, app_params, app_filter = cfactory[name]["use"], \
        cfactory[name]["params"], cfactory[name]["filter"]
    if app_filter:
        for mname, mattrs in mfactory.items():
            muse, mparams, mnext = mattrs["use"], mattrs["params"], mattrs["next"]
            if app_filter == mname :
                if mnext and mnext != name:
                    # 配置冲突，middleware 的 next 属性指定的 app, 该 app 的 filter 属性又指定了另外的 middleware
                    raise ConfigurationError("'next' attribute %r invalid." % mnext)
                app = make_app_from_cfactory(deploy_ctx, name)
                filter = make_filter_from_mfactory(deploy_ctx, mname)
                if not app:
                    raise ConfigurationError("load app %r failure." % name)
                if not filter:
                    raise ConfigurationError("load filter %r failure." % mname)
                return filter(app)
    else:
        app = make_app_from_cfactory(deploy_ctx, name)
        if app is None:
            raise ConfigurationError("load app %r failure." % name)
        return app

def get_app(deploy_ctx, name):
    app = get_app_from_mfactory(deploy_ctx, name)
    if app is not None:
        return app
    app = get_app_from_afactory(deploy_ctx, name)
    if app is not None:
        return app
    app = get_app_from_cfactory(deploy_ctx, name)
    if app is not None:
        return app

def get_all_apps(deploy_ctx):
    mfactory = deploy_ctx["filter_factory"]
    afactory = deploy_ctx["app_factory"]
    cfactory = deploy_ctx["composite_factory"]
    all_app_names = set(map(lambda x : x[0], filter(lambda x : x[1]["next"], mfactory.items())) + afactory.keys() + cfactory.keys())
    apps = dict(filter(lambda x : x[1], \
                       map(lambda app_name: (app_name, get_app(deploy_ctx, app_name)), all_app_names)))
    return apps

class DefaultVarsContainer(UserDict, object):

    implements(IDefaultVarFactory)

    def __init__(self, *args, **kargs):
        self.data = dict(*args, **kargs)

    def __getitem__(self, key):
        if self.__contains__(key):
            return super(DefaultVarsContainer, self).__getitem__(key)
        else:
            return ""

def get_context_from_zcml(package=None, zcml="configure.zcml", zcml_context=None):
    '''
    如果 package 不提供将不能够在ZCML配置中使用相对路径
    '''

    zcml = zcml or "configure.zcml"
    config_file = None
    if package is None:
        config_file = os.path.abspath(zcml)
        file_dir = os.path.dirname(config_file)
    else:
        if isinstance(package, basestring):
            # 附加当前路径到搜索路径中
            sys.path.append(os.getcwd())
            __import__(package, globals(), locals(), [], -1)
            package = sys.modules[package]
        config_file = os.path.join(os.path.dirname(package.__file__), zcml)
        file_dir = os.path.dirname(os.path.dirname(package.__file__))

    context = {}
    global_conf = {}
    global_conf["__file__"] = config_file
    mfactory = MiddlewareFactory()
    afactory = AppFactory()
    cfactory = CompositeFactory()
    ofactory = ObjectFactory()
    ofactory.name = config_file
    sfactory = ServerFactory()
    vars_factory = DefaultVarsContainer()

    vars_factory["__dir__"] = file_dir
    vars_factory["__file__"] = config_file

    # 得到loggers
    lobj = LoggingObject()
    provideUtility(lobj, ILoggingObject)

    zcml_context = zcml_context or ConfigurationMachine()
    zcml_context.name = config_file
    zcml_context.global_conf = global_conf

    provideUtility(mfactory, IMiddlewareFactory, zcml_context.name)
    provideUtility(afactory, IAppFactory, zcml_context.name)
    provideUtility(cfactory, ICompositeFactory, zcml_context.name)
    provideUtility(ofactory, IObjectFactory, zcml_context.name)
    provideUtility(sfactory, IServerFactory, zcml_context.name)
    provideUtility(vars_factory, IDefaultVarFactory, zcml_context.name)

    xmlconfig.registerCommonDirectives(zcml_context)

    if package:
        zcml_context.package = package

    if isinstance(zcml, basestring):
        zcml = file(config_file)
    elif not hasattr(zcml, "read"):
        raise ValueError("`zcml` argument invalid")

    xmlconfig.processxmlfile(zcml, zcml_context)
    zcml_context.execute_actions(clear=False)

    vars_factory.pop("loader", None)

    global_conf.update(vars_factory)
    # 重新设置内置变量值，防止被 default 指令内的同名值覆盖
    global_conf["__dir__"] = file_dir
    global_conf["__file__"] = config_file
    
    # 如果配置文件没有指定 <server> 指令, 则添加一个默认的, 默认使用 paste 的 http server
    if len(sfactory) == 0:
        sfactory["main"] = {
                  'entry_point': "egg:Paste#http",
                  'config': {"app" : "main"},
                  'params': {"host" : "0.0.0.0", "port" : 7010}
                  }
    context["vars_factory"] = vars_factory
    context["server_factory"] = sfactory
    context["filter_factory"] = mfactory
    context["app_factory"] = afactory
    context["composite_factory"] = cfactory
    context["object_factory"] = ofactory
    context["global_conf"] = global_conf
    context["package"] = package
    context["logging"] = lobj
    return context

def get_app_from_zcml(zcml, name):
    zcml = os.path.abspath(zcml)
    deploy_ctx = get_context_from_zcml(zcml=zcml)
    return get_app(deploy_ctx, name)

def get_object_from_zcml(zcml, name):
    zcml = os.path.abspath(zcml)
    deploy_ctx = get_context_from_zcml(zcml=zcml)
    return make_object_from_ofactory(deploy_ctx, name)

def get_filter_from_zcml(zcml, name):
    zcml = os.path.abspath(zcml)
    deploy_ctx = get_context_from_zcml(zcml=zcml)
    return make_filter_from_mfactory(deploy_ctx, name)

def get_server_from_zcml(zcml, name):
    zcml = os.path.abspath(zcml)
    deploy_ctx = get_context_from_zcml(zcml=zcml)
    return make_server_from_sfactory(deploy_ctx, name)

def logging_from_zcml_context(context):
    '''
    用 zcml 的 context 对象配置 logging
    '''
    
    lobj = context['logging']
    if lobj.level is None:
        return

    LEVELS = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    # 初始化Logging
    logging.basicConfig(level = LEVELS.get(lobj.level.lower(), logging.NOTSET))

    # create formmatters object
    formatters = {}
    for n,v in lobj.formatters.iteritems():
        if v['args'].strip():
            args = eval(v['args'] + ",")
        else:
            args = ()
        formatters[n] = v['cls'](*args)

    handlers = {}
    for n,v in lobj.handlers.iteritems():
        if v['args'].strip():
            args = eval(v['args'] + ",")
        else:
            args = ()
        handler = v['cls'](*args)
        handler.setLevel(LEVELS.get(v['level'].lower(), logging.NOTSET))
        handler.setFormatter(formatters.get(v['formatter']))
        handlers[n] = handler
        logging.root.addHandler(handler)

    for n,v in lobj.loggers.iteritems():
        # 无效的Logger名
        if not n in lobj.available_loggers:
            continue
        logger = logging.getLogger(n)
        logger.setLevel(LEVELS.get(v['level'].lower(), logging.NOTSET))
        if not v['qualname'] is None:
            logger.name = v['qualname']
        logger.propagate = v['propagate']

        for i in v['handlers']:
            logger.addHandler(handlers.get(i))

        # FIXME 确定是否需要替换RootLogger
        logging.root.manager.loggerDict[n] = logger

def run_server_from_zcml(package=None, zcml="configure.zcml", zcml_context=None, server_name='main'):
    """
    从 zcml 配置文件运行 HTTP 服务器

    :param package: 包对象或包名
    :param zcml: zcml 文件名,可以是类似 File 的对象或是文件名(非绝对路径).默认值为: "configure.zcml"
    :type zcml: str or file like object
    """

    deploy_ctx = get_context_from_zcml(package, zcml=zcml, zcml_context=zcml_context)
    server_runner = make_server_from_sfactory(deploy_ctx, server_name)
    logging_from_zcml_context(deploy_ctx)
    return server_runner()

class LoadableObjectType(_ObjectType):

    name = "object"
    egg_protocols = ["khan.loadable_objects"]
    config_prefixes = ["khan:object", "object"]

    def invoke(self, context):
        if context.protocol == "khan.loadable_objects":
            return fix_call(context.object, context.global_conf, **context.local_conf)
        else:
            assert 0, "Protocol %r unknown" % context.protocol

def make_dict_object(global_conf, **items):
    """
    Paste EGG entry point::

        dict

    PasteDeploy example::

        [object:dict]
        use = egg:khan#dict
        key1 = value1
        key2 = value2

    .. note::

        key 中的 '-' 会被替换为 '_'  . really ??
    """

    data = {}
    for name, value in items.items():
        #if name.find( '-' ) != -1:
        data[ re.sub( r'-', '_', name ) ] = value

    return data

def get_from_egg(package, name = "main", egg_protocols = []):
    entry = None

    for egg_protocol in egg_protocols:
        pkg_resources.require(package)
        entry = pkg_resources.get_entry_info(
             package, egg_protocol,
             name)
        if not entry is None:
            break

    if entry:
        try:
            return entry.load()
        except:
            logging.error('load entry failed: %s' % entry, exc_info=True)

def get_server_from_egg(global_conf, package, name = "main", **params):
    maker = get_from_egg(package, name, ["paste.server_runner"])
    if maker:
        return lambda app: maker(app, global_conf, **params)
    else:
        maker = get_from_egg(package, name, ["paste.server_factory"])
        if maker:
            return maker(global_conf, **params)

def get_app_from_egg(global_conf, package, name = "main", **params):
    maker = get_from_egg(package, name, ["paste.app_factory"])
    if maker:
        return maker(global_conf, **params)
    else:
        maker = get_from_egg(package, name, ["paste.composite_factory"])
        if maker:
            return maker(global_conf.get("loader"), global_conf, **params)

def get_filter_from_egg(global_conf, package, name = "main", **params):
    maker = get_from_egg(package, name, ["paste.filter_factory"])
    if maker:
        return maker(global_conf, **params)
    else:
        maker = get_from_egg(package, name, ["paste.filter_app_factory"])
        if maker:
            return lambda app : maker(app, global_conf, **params)

def get_object_from_egg(global_conf, package, name = "main", **params):
    maker = get_from_egg(package, name, ["khan.loadable_objects"])
    if maker:
        return maker(global_conf, **params)

def get_object_from_uri(global_conf, uri, obj_type = objectTypes.APP, **params):
    '''
    从资源连接中，得到 object 对象

    :param global_conf: 全局配置
    :type global_conf: dict

    :param uri: 资源连接
    :type uri: String

    :param obj_type: 设定读取的 object context 类型
    :type obj_type: objectTypes

    :rtype: object context or None( 如果没有找到的情况下 )
    '''
    if ":" in uri:
        pos = uri.find(':')
        protocol_name = uri[0 : pos].lower()
        protocol_content = uri[pos + 1 : ] 
        if protocol_name == "egg":
            if "#" in protocol_content:
                egg_package, egg_name = protocol_content.split("#")
            else:
                egg_package = protocol_content
                egg_name = "main"

            if obj_type == objectTypes.APP:
                return get_app_from_egg(global_conf, egg_package, egg_name, **params)
            elif obj_type == objectTypes.FILTER:
                return get_filter_from_egg(global_conf, egg_package, egg_name, **params)
            elif obj_type == objectTypes.SERVER:
                return get_server_from_egg(global_conf, egg_package, egg_name, **params)
            elif obj_type == objectTypes.OBJECT:
                return get_object_from_egg(global_conf, egg_package, egg_name, **params)

        # zcml 和 config 协议相同
        elif protocol_name == "config" or protocol_name == 'zcml':
            if "#" in protocol_content:
                zcml, name = protocol_content.split("#")
            else:
                zcml = protocol_content
                name = "main"

            # 如果 zcml 不是以 "/" 开头的话就使用相对路径
            if not zcml.startswith(os.sep):
                zcml = os.path.abspath(os.path.join(os.path.dirname(global_conf["__file__"]), zcml))
            if zcml == global_conf["__file__"]:
                loader = global_conf.get("loader")
                if not loader:
                    return
                if obj_type == objectTypes.APP:
                    return loader.get_app(name)
                elif obj_type == objectTypes.FILTER:
                    return loader.get_filter(name)
                elif obj_type == objectTypes.SERVER:
                    return loader.get_server(name)
                elif obj_type == objectTypes.OBJECT:
                    return loader.get_object(name)
            else:
                if obj_type == objectTypes.APP:
                    return get_app_from_zcml(zcml, name)
                elif obj_type == objectTypes.FILTER:
                    return get_filter_from_zcml(zcml, name)
                elif obj_type == objectTypes.SERVER:
                    return get_server_from_zcml(zcml, name)
                elif obj_type == objectTypes.OBJECT:
                    return get_object_from_zcml(zcml, name)

        elif protocol_name == "ref":
            name = protocol_content
            loader = global_conf.get("loader")
            if not loader:
                return
            if obj_type == objectTypes.APP:
                return loader.get_app(name)
            elif obj_type == objectTypes.FILTER:
                return loader.get_filter(name)
            elif obj_type == objectTypes.SERVER:
                return loader.get_server(name)
            elif obj_type == objectTypes.OBJECT:
                return loader.get_object(name)

        else:
            raise ConfigurationError(uri)

    # 如果没有冒号，就当作是未知，蚕食配置
    else:
        name = uri
        loader = global_conf.get("loader")
        if not loader:
            logging.warn( 'global config context had not a loader without protocol' )
            return

        if obj_type == objectTypes.APP:
            return loader.get_app(name)
        elif obj_type == objectTypes.FILTER:
            return loader.get_filter(name)
        elif obj_type == objectTypes.SERVER:
            return loader.get_server(name)
        elif obj_type == objectTypes.OBJECT:
            return loader.get_object(name)

def loadobject(uri, name=None, global_conf = None, **kw):
    """
    加载一个 object, 该 object 必须声明在 egg 中, 例如::

        "khan.loadable_objects" : [
            "store = khan.store:make_store_object",
        ]

    (NO TESTCAST)

    从配置文件加载::

        store_obj = loadobject("config:/path/to/config.ini", "store")

    从 EGG 加载::

        store_obj = loadobject("egg:khan", "store")
    """

    if name:
        # 如果 uri 中已经有 #name 则忽略 `name` 参数, 如果 uri 中不包括 ':' (既不指定协议类型，也同样忽略 `name` 参数
        if "#" not in uri and ":" in uri:
            uri = uri + "#" + name
    if global_conf:
        if "loader" in global_conf:
            return get_object_from_uri(global_conf, uri, objectTypes.OBJECT, **kw)
        else:
            return loadobj(LoadableObjectType(), uri, name, **kw)
    return loadobj(LoadableObjectType(), uri, name, **kw)

def loadapp(uri, name=None, global_conf = None, **kw):
    if name:
        # 如果 uri 中已经有 #name 则忽略 `name` 参数, 如果 uri 中不包括 ':' (既不指定协议类型，也同样忽略 `name` 参数
        if "#" not in uri and ":" in uri:
            uri = uri + "#" + name
    if global_conf:
        if "loader" in global_conf:
            return get_object_from_uri(global_conf, uri, objectTypes.APP, **kw)
        else:
            return _loadapp(uri, name, **kw)
    return _loadapp(uri, name, **kw)

def loadfilter(uri, name=None, global_conf = None, **kw):
    if name:
        # 如果 uri 中已经有 #name 则忽略 `name` 参数, 如果 uri 中不包括 ':' (既不指定协议类型，也同样忽略 `name` 参数
        if "#" not in uri and ":" in uri:
            uri = uri + "#" + name
    if global_conf:
        if "loader" in global_conf:
            return get_object_from_uri(global_conf, uri, objectTypes.FILTER, **kw)
        else:
            return _loadfilter(uri, name, **kw)
    return _loadfilter(uri, name, **kw)

def loadserver(uri, name=None, global_conf = None, **kw):
    if name:
        # 如果 uri 中已经有 #name 则忽略 `name` 参数, 如果 uri 中不包括 ':' (既不指定协议类型，也同样忽略 `name` 参数
        if "#" not in uri and ":" in uri:
            uri = uri + "#" + name
    if global_conf:
        if "loader" in global_conf:
            return get_object_from_uri(global_conf, uri, objectTypes.SERVER, **kw)
        else:
            return _loadserver(uri, name, **kw)
    return _loadserver(uri, name, **kw)

class Loader(object):

    def __init__(self, deploy_ctx, self_name):
        self.deploy_ctx = deploy_ctx.copy()
        self.self_name = self_name

    def get_app(self, name=None, global_conf=None):
        if not name:
            return
        if name == self.self_name:
            # 禁止获取自己，因为会造成无限递归
            raise ValueError("app name `%s` invalid, can't load self" % name)
        deploy_ctx = self.deploy_ctx
        if global_conf:
            deploy_ctx["global_conf"] = global_conf
        return get_app(deploy_ctx, name)

    def get_filter(self, name=None, global_conf=None):
        if not name:
            return
        if name == self.self_name:
            # 禁止获取自己，因为会造成无限递归
            raise ValueError("middleware name `%s` invalid, can't load self" % name)
        deploy_ctx = self.deploy_ctx
        if global_conf:
            deploy_ctx["global_conf"] = global_conf
        return make_filter_from_mfactory(deploy_ctx, name)

    def get_object(self, name=None, global_conf=None):
        if not name:
            return
        if name == self.self_name:
            # 禁止获取自己，因为会造成无限递归
            raise ValueError("object name `%s` invalid, can't load self" % name)
        deploy_ctx = self.deploy_ctx
        if global_conf:
            deploy_ctx["global_conf"] = global_conf
        return make_object_from_ofactory(deploy_ctx, name)

    def get_server(self, name=None, global_conf=None):
        if not name:
            return
        if name == self.self_name:
            # 禁止获取自己，因为会造成无限递归
            raise ValueError("object name `%s` invalid, can't load self" % name)
        deploy_ctx = self.deploy_ctx
        if global_conf:
            deploy_ctx["global_conf"] = global_conf
        return make_server_from_sfactory(deploy_ctx, name)

class MiddlewareFactory(UserDict):

    implements(IMiddlewareFactory)

    def __init__(self, *args, **kargs):
        self.data = dict(*args, **kargs)

class AppFactory(UserDict):

    implements(IAppFactory)

    def __init__(self, *args, **kargs):
        self.data = dict(*args, **kargs)

class CompositeFactory(UserDict):

    implements(ICompositeFactory)

    def __init__(self, *args, **kargs):
        self.data = dict(*args, **kargs)

class ObjectFactory(UserDict):

    implements(IObjectFactory)

    def __init__(self, *args, **kargs):
        self.data = dict(*args, **kargs)

class ServerFactory(UserDict):

    implements(IServerFactory)

    def __init__(self, *args, **kargs):
        self.data = dict(*args, **kargs)

class LoggingObject(object):

    implements(ILoggingObject)

    def __init__(self):
        self.loggers = {}
        self.handlers = {}
        self.formatters = {}
        self.level = None
        self.available_loggers = []
        self.data = {}

class EnvironLoadable(object):
    """
    FIXME: 权宜之计！ 为了使 khan.shell 命令时所有的 StackedObject 可用
    """

    PATH_HOOK = "/_test_vars"

    def __init__(self, app):
        self.app = app
        self._logger = logging.getLogger(self.__class__.__name__)

    def __call__(self, environ, start_response):
        if "paste.testing_variables" in environ:
            if environ["PATH_INFO"] == self.PATH_HOOK:
                restorer.save_registry_state(environ)
                start_response("200 OK", [("Content-type", "text/plain")])
                return ["%s" % restorer.get_request_id(environ)]
            else:
                return self.app(environ, start_response)
        else:
            return self.app(environ, start_response)

def make_environloadable_middleware(global_conf):
    def filter(app):
        return EnvironLoadable(app)
    return filter

class EnvironLoader(object):
    """
    load environ from zcml
    """

    def __init__(self, package = None, zcml = None, logging = False, server_name = "main"):
        self.package = package
        self.zcml = zcml
        self.logging = logging
        self.server_name = server_name

    def open(self):
        package = self.package
        zcml = self.zcml
        logging = self.logging
        server_name = self.server_name
        if not zcml and not package:
            raise ValueError("You must give a `package` or `ZCML` argument")
        here_dir = os.getcwd()
        zcml_context = get_context_from_zcml(package, zcml = zcml)
        if logging:
            # Configure logging from the config file
            logging_from_zcml_context(zcml_context)

        # Load locals and populate with objects for use in shell
        sys.path.insert(0, here_dir)

        # Load the wsgi app first so that everything is initialized right
        wsgiapp = make_app_from_server(zcml_context, server_name)

        if not wsgiapp:
            raise TypeError("No valid app related with server(name='%s')" % server_name)

        """
        registry = Registry()
        extra_environ={'paste.throw_errors': False, 'paste.registry': registry}
        request_id = restorer.get_request_id(extra_environ)
        test_app = TestApp(RegistryManager(EvalException(wsgiapp)), extra_environ=extra_environ)
        restorer.restoration_begin(request_id)
        res = test_app.get('/_test_vars', extra_environ=extra_environ, expect_errors=True)
        """

        test_app = TestApp(wsgiapp)
        # FIXME: test_app.get 为什么会发送两次请求?
        # Query the test app to setup the environment
        tresponse = test_app.get(EnvironLoadable.PATH_HOOK, status = "*")
        try:
            request_id = int(tresponse.body)
        except:
            wsgiapp = EnvironLoadable(wsgiapp)
            test_app = TestApp(wsgiapp)
            tresponse = test_app.get(EnvironLoadable.PATH_HOOK, status = "*")
            try:
                request_id = int(tresponse.body)
            except:
                raise TypeError("Can't load project environ")
        # Disable restoration during test_app requests
        test_app.pre_request_hook = lambda self: restorer.restoration_end()
        test_app.post_request_hook = lambda self: restorer.restoration_begin(request_id)
        # Restore the state of the KhanSite special objects
        # (StackedObjectProxies)
        restorer.restoration_begin(request_id)
        return test_app, zcml_context

    def close(self):
        restorer.restoration_end()

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()
        if traceback is None:
            return False

